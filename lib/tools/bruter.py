import os
import sys
import socket
import thirdparty.dns
import thirdparty.dns.resolver
import thirdparty.dns.exception
import thirdparty.requests as requests

from lib.core.dnslookup import DNSLookup
from lib.core.settings import config, quest
from thirdparty.dns.resolver import Resolver
from lib.parse.cmdline import parse_args, parse_error
from lib.parse.colors import white, green, red, yellow, end, info, que, bad, good, run

def donames_list():
	donames = []
	file_ = "\data\domains.txt"
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
	seen = set()
	print (que + 'Bruteforcing domain extensions and getting the DNS:')
	for item in checking:
		try:
			nameservers = thirdparty.dns.resolver.query(item,'NS')
			for data in nameservers:
				data = str(data).rstrip('.')
				if 'cloudflare' not in data and item not in seen:
						seen.add(item)
						good_dns.append(data)
						print ('   ' + good + str(data) + ' from: ' + item)
				else:
					print('   ' + bad + 'DNS appear to belong Cloudflare')
		except thirdparty.dns.resolver.NXDOMAIN:
			pass
		except thirdparty.dns.resolver.Timeout:
			pass
		except thirdparty.dns.exception.DNSException:
			pass
	return good_dns