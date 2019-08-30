import os
import sys
import socket
import thirdparty.dns
import thirdparty.dns.resolver
import thirdparty.dns.exception
import thirdparty.requests as requests
from lib.parse.cmdline import parse_args, parse_error
from lib.parse.colors import white, green, red, yellow, end, info, que, bad, good, run
from lib.core.settings import config
from thirdparty.html_similarity import similarity
from thirdparty.dns.resolver import Resolver


def scan(domain,ns):
	try:
		print("\n" + yellow +"Tracking IP (Auto DIG)...\n")
		print(que + "Checking if {0} is similar to {1}".format(ns, domain))
		test1 = requests.get('http://' + domain, timeout=config['http_timeout_seconds'])
		test2 = requests.get('http://' + ns, timeout=config['http_timeout_seconds'])
		page_similarity2 = similarity(test1.text, test2.text)
		if page_similarity2 > config['response_similarity_threshold']:
			print ('   ' + good + 'HTML content is %d%% structurally similar to: %s' % (round(100 *page_similarity2, 2), domain))
		else:
			print ('   ' + bad + 'Sorry, but HTML content is %d%% structurally similar to: %s' % (round(100 *page_similarity2, 2), domain))
	except requests.exceptions.Timeout:
		print('   ' + bad + 'Connection cannot be established with: %s'% (ns))

def DNSLookup(domain, ns):
	sys_r = Resolver()
	dns = [ns]
	try:
		dream_dns = [item.address for server in dns for item in sys_r.query(server)]
		dream_r = Resolver()
		dream_r.nameservers = dream_dns
		answer = dream_r.query(domain, 'A')
		for A in answer.rrset.items:
			return A
	except Exception:
		print (que + 'Using DIG to get the real IP')
		print('   ' + bad + 'IP not found using DNS Lookup')