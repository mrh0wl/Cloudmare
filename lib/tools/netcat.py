import os
import sys
import socket
import thirdparty.six as six
import thirdparty.requests as requests
import thirdparty.urllib3 as urllib3

from lib.core.settings import config, quest
from thirdparty.html_similarity import similarity
from lib.parse.cmdline import parse_args, parse_error
from lib.core.dnslookup import Checking_DNS
from lib.parse.colors import white, green, red, yellow, end, info, que, bad, good, run

def netcat(domain, ns, count):
	if count == 0:
		ip = socket.gethostbyname(ns)
	elif count > 0:
		A = Checking_DNS(domain, ns)
		ip = str(A)
	url = 'http://' + domain
	page = requests.get(url, timeout=config['http_timeout_seconds'])
	hncat = page.url.replace('https://' or 'http://', '').split('/')[0]
	home = page.url.replace('https://' or 'http://', '').split(hncat)[1]
	print (que + 'Connecting %s using as Host Header: %s'% (ip, domain))
	try:	
		data = requests.get('http://' + ip + home, headers={'host': hncat},timeout=config['http_timeout_seconds'])
		count =+ 1
		if data.status_code == 200:
			count =+ 1
			sim = similarity(data.text, page.text)
			if sim > config['response_similarity_threshold']:
				print ("   " + good + 'The connect has %d%% similarity to: %s' % (round(100 *sim, 2), url))
				print ("   " + good + '%s is the real IP'%ip)
				try:
					quest(question='\n' + info + 'IP found. Do yo want to stop tests? y/n: ', doY='sys.exit()', doN="pass")
				except KeyboardInterrupt:
					sys.exit()
			else:
				print ("   " + bad +'The connect has %d%% similarity to: %s' % (round(100 *sim, 2), url))
				print ("   " + bad +"%s is not the IP" %ip)
		else:
			print ("   " + bad +"An unexpected response code has occurred")
	except requests.exceptions.SSLError:
		print("   " + bad +'Error handshaking with SSL')
	except requests.exceptions.ReadTimeout:
		print("   " + bad +"Connection Timeout to: %s"% ip)
	except requests.ConnectTimeout:
		print("   " + bad +"Connection Timeout to: %s"% ip)