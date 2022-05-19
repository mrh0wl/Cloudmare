import random
import subprocess
import thirdparty.requests as requests
from lib.parse.colors import Y, W, B, R, que, bad, good, tab
from lib.parse.settings import config
from thirdparty.html_similarity import similarity
from thirdparty.dns.resolver import Resolver

def scan(domain, host, userAgent, randomAgent, header):
	headers = dict(x.replace(' ', '').split(':') for x in header.split(',')) if header != None else {}
	headers.update({'User-agent': random.choice(open("data/txt/random_agents.txt").readlines()).rstrip("\n")}) if randomAgent == True else ''
	headers.update({'User-agent': userAgent}) if userAgent != None else ''
	try:
		print("\n" + Y + "Attempting to track real IP using: %s\n" % host)
		print(que + "Checking if {0} is similar to {1}".format(host, domain))
		get_domain = requests.get('http://' + domain, headers=headers, timeout=config['http_timeout_seconds'])
		get_host = requests.get('http://' + host, headers=headers, timeout=config['http_timeout_seconds'])
		page_similarity = similarity(get_domain.text, get_host.text)
		if page_similarity > config['response_similarity_threshold']:
			print (tab + good + 'HTML content is %d%% structurally similar to: %s' % (round(100 *page_similarity, 2), domain))
		else:
			print (tab + bad + 'Sorry, but HTML content is %d%% structurally similar to: %s' % (round(100 *page_similarity, 2), domain))
	except Exception:
		print(tab + bad + 'Connection cannot be established with: %s'% (host))


def DNSLookup(domain, host):
	isAndroid = subprocess.check_output(['uname', '-o']).strip() == b'Android'
	sys_r = Resolver(filename='/data/data/com.termux/files/usr/etc/resolv.conf') if isAndroid else Resolver()
	dns = [host]
	try:
		dream_dns = [item.address for server in dns for item in sys_r.query(server)]
		dream_r = Resolver()
		dream_r.nameservers = dream_dns
		answer = dream_r.query(domain, 'A')
		for A in answer.rrset.items:
			return A
	except Exception:
		pass