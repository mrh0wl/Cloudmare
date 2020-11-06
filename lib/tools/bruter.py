#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import thirdparty.dns
import thirdparty.dns.resolver
import thirdparty.dns.exception
import thirdparty.requests as requests

from lib.analyzer.ispcheck import ISPCheck
from lib.parse.settings import config
from lib.parse.colors import que, bad, good, tab

def donames_list():
	donames = []
	file_ = "/data/txt/domains.txt"
	path = os.getcwd()+file_
	with open (path,'r') as f:
		domlist = [line.strip() for line in f]
		for item in domlist:
			donames.append(item)
	return donames

def bruter(domain):
	good_check = []
	donames = donames_list()
	url = 'http://' + domain
	try:
		page = requests.get(url, timeout=config['http_timeout_seconds'])
		http = 'http://' if 'http://' in page.url else 'https://'
		host = page.url.replace(http, '').split('/')[0]
		webname = host.split('.')[1].replace('.', '') if 'www' in host else host.split('.')[0]
		for i in donames:
			domain = webname + i if '.' not in webname else webname.split(0)
			if url.replace('http://', '') not in domain:
				good_check.append(domain)
		return good_check
	except requests.exceptions.SSLError:
		print("   " + bad +'Error handshaking with SSL')
	except requests.exceptions.ReadTimeout:
		print("   " + bad +"Connection Timeout")
	except requests.ConnectTimeout:
		print("   " + bad +"Connection Timeout ")

def nameserver(domain):
	checking = bruter(domain)
	good_dns = []
	print (que + 'Bruteforcing domain extensions and getting DNS records')
	for item in checking:
		try:
			nameservers = thirdparty.dns.resolver.query(item,'NS')
			MX = thirdparty.dns.resolver.query(item,'MX')
			for data in nameservers:
				data = str(data).rstrip('.')
				for record in MX:
					record = str(record).split(' ')[1].rstrip('.')
					DataisCloud = ISPCheck(data)
					RecordisCloud = ISPCheck(record)
					if DataisCloud == None:
						if data not in good_dns:
							good_dns.append(data)
							print (tab + good + 'NS Record: ' + str(data) + ' from: ' + item)
					else:
						print(tab + bad + 'NS Record: ' + str(data) + ' from: ' + item + DataisCloud)
						
					if RecordisCloud == None:
						if record not in good_dns:
							good_dns.append(record)
							print (tab + good + 'MX Record: ' + str(record) + ' from: ' + item)
					else:
						print(tab + bad + 'MX Record: ' + str(record) + ' from: ' + item + RecordisCloud)
		except thirdparty.dns.resolver.NXDOMAIN as e:
			print(tab + bad + '%s'%e)
		except thirdparty.dns.resolver.Timeout as e:
			pass
		except thirdparty.dns.exception.DNSException as e:
			pass
	return good_dns