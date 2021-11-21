#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import socket
import random
import thirdparty.requests as requests
import thirdparty.urllib3 as urllib3

from lib.parse.settings import config, quest, PYVERSION
from lib.analyzer.ispcheck import ISPCheck
from thirdparty.html_similarity import similarity
from lib.analyzer.dnslookup import DNSLookup
from lib.parse.colors import info, que, bad, good, tab

urllib3.disable_warnings()

def netcat(domain, host, ignoreRedir, userAgent, randomAgent, header, count):
	headers = dict(x.replace(' ', '').split(':') for x in header.split(',')) if header != None else {}
	headers.update({'User-agent': random.choice(open("data/txt/random_agents.txt").readlines()).rstrip("\n"),}) if randomAgent == True else ''
	headers.update({'User-agent': userAgent}) if userAgent != None else ''
	schemas = ['http://', 'https://']
	A = DNSLookup(domain, host)
	try:
		ip = socket.gethostbyname(str(host)) if count == 0 else str(A)
	except:
		print(tab + bad + "Error Resolving host: "+ str(host))
	if not A:
		print (que + 'Using DIG to get the real IP')
		print('   ' + bad + 'IP not found using DNS Lookup')
	try:
		isCloud = ISPCheck(ip)
		if isCloud != None:
			print(tab + info + ip + isCloud + '. Closing connection.')
		else:
			print (que + 'Connecting %s using as Host Header: %s'% (ip, domain))
			count =+ 1
			for i in range(len(schemas)):
				page = requests.get(schemas[i] + domain, timeout=config['http_timeout_seconds'])
				hncat = page.url.replace(schemas[i], '').split('/')[0]
				headers.update(host = hncat)
				home = page.url.replace(schemas[i], '').split(hncat)[1]
				data = requests.get(schemas[i] + ip, headers=headers,timeout=config['http_timeout_seconds'], allow_redirects=False, verify=False)
				if data.status_code in [301, 302]:
					print(tab + info + "%s redirects to: %s"% (schemas[i] + ip, data.headers['Location']))
					question = ignoreRedir if ignoreRedir != True else input(tab + info + 'Do yo want to redirect? y/n: ') if PYVERSION.startswith('3') else raw_input(tab + info + 'Do yo want to redirect? y/n: ')
					redir = True if question in ['y', 'yes', 'ye'] else ignoreRedir if ignoreRedir != True else False
					try:
						data = requests.get(schemas[i] + ip, headers=headers,timeout=config['http_timeout_seconds'], allow_redirects=redir, verify=False)
					except:
						if question in ['y', 'yes', 'ye']:
							print(tab + bad +'Error while connecting to: %s'%data.headers['Location'])
				if data.status_code == 200:
					count =+ 1
					sim = similarity(data.text, page.text)
					if sim > config['response_similarity_threshold']:
						print(tab + good + 'The connection has %d%% similarity to: %s' % (round(100 *sim, 2), domain))
						print(tab + good + '%s is the real IP'%ip)
						try:
							quest(question='\n' + info + 'IP found. Do yo want to stop tests? y/n: ', doY='sys.exit()', doN="pass")
						except KeyboardInterrupt:
							sys.exit()
					else:
						print(tab + bad +'The connect has %d%% similarity to: %s' % (round(100 *sim, 2), domain))
						print(tab + bad +"%s is not the IP" %ip)
						print('\n\n'+data.text)
				else:
					print(tab + bad + 'Unexpected status code [%s] occurred at: %s' % (data.status_code, schemas[i] + ip))
	except requests.exceptions.SSLError:
		print(tab + bad +'Error handshaking with SSL')
	except requests.exceptions.ReadTimeout:
		print(tab + bad +"Connection ReadTimeout to: %s"% ip)
	except requests.ConnectTimeout:
		print(tab + bad +"Connection Timeout to: %s"% ip)
	except requests.exceptions.ConnectionError:
		print(tab + bad +"Connection Error to: %s"% ip)
	except requests.exceptions.InvalidHeader as e:
		print(tab + bad +"Error using header: %s" % str(e))
	except Exception as e:
		print(tab + bad +"An unexpected error occurred: %s" % str(e))
