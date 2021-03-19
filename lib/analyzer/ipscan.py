from __future__ import print_function
from __future__ import absolute_import

from lib.parse.settings import config, checkImports, PYVERSION
from lib.parse.colors import W, G, R, Y, end, info, que, bad, good, run, tab
from lib.parse.cmdline import parser_cmd
import random

while True:
	try:
		import thirdparty.requests as requests
		from lib.tools.netcat import netcat
		from lib.tools.bruter import nameserver
		from lib.tools.censys import censys
		from thirdparty.html_similarity import similarity
		from lib.analyzer.dnslookup import scan, DNSLookup
		from thirdparty.dns.resolver import Resolver
		from lib.tools import sublist3r
		break
	except Exception as e:
		err = e.name if PYVERSION.startswith('3') else str(e).split('named')[1]
		checkImports(err).downloadLib()

def IPscan(domain, ns, A, userAgent, randomAgent, header, args):
		url = 'http://' + domain
		headers = dict(x.replace(' ', '').split(':') for x in header.split(',')) if header != None else {}
		headers.update({'User-agent': random.choice(open("data/txt/random_agents.txt").readlines()).rstrip("\n"),}) if randomAgent == True else ''
		headers.update({'User-agent': userAgent}) if userAgent != None else ''
		if A != None:
			try:
				print (que + 'Using DIG to get the real IP')
				print (tab + good + 'Possible IP: %s' % str(A))
				print(que + 'Retrieving target homepage at: %s' % url)
				org_response = requests.get(url, headers=headers, timeout=config['http_timeout_seconds'])
				if org_response.status_code != 200:
					print (tab + bad + 'Responded with an unexpected HTTP status code')
				if org_response.url != url:
					print (tab + good + '%s Rirects to %s' % (url, org_response.url))
				try:
					sec_response = requests.get('http://' + str(A), headers=headers, timeout=config['http_timeout_seconds'])
					if sec_response.status_code != 200:
						print (tab + bad + 'Responded with an unexpected HTTP status code')
					else:
						page_similarity = similarity(sec_response.text, org_response.text)
						if page_similarity > config['response_similarity_threshold']:
							print (que + 'Testing if source body is the same in both websites')
							print (tab + good + ' HTML content is %d%% structurally similar to: %s' % (round(100 *page_similarity, 2), org_response.url))
				except Exception:
					print(tab + bad +"Connection Timeout")
				netcat(domain, ns, args.ignoreRedirects,userAgent, randomAgent, args.headers, count=+1)
				return org_response
			except requests.exceptions.SSLError:
				print(tab + bad +'Error handshaking with SSL')
			except requests.exceptions.ReadTimeout:
				print(tab + bad +"Connection Timeout")
			except requests.ConnectTimeout:
				print(tab + bad +"Connection Timeout")
			except requests.exceptions.Timeout:
				print(tab + bad + "%s timed out after %d seconds" % (url, config['http_timeout_seconds']))
			except requests.exceptions.RequestException:
				print(tab + bad + "Failed to retrieve: %s" % url)
