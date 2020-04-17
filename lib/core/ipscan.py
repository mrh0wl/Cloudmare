from __future__ import print_function
from __future__ import absolute_import

from lib.parse.settings import quest, logotype, osclear, config, checkImports
from lib.parse.colors import white, green, red, yellow, end, info, que, bad, good, run
import os, sys

while True:
	try:
		import thirdparty.requests as requests
		from lib.parse.cmdline import parse_args, parse_error
		from lib.tools.netcat import netcat
		from lib.tools.bruter import nameserver
		from lib.tools.censys import censys
		from thirdparty.html_similarity import similarity
		from lib.core.dnslookup import scan, DNSLookup
		from thirdparty.dns.resolver import Resolver
		from lib.tools.subdomain_finder import subdomain_tracking
		break
	except ImportError as e:
		isPy = sys.version_info[0]
		if isPy == 3:
			err = e.name
		else:
			err = str(e).split('named')[1]
		checkImports(err).downloadLib()

def make_list(domain):
	try:
		ip_list = subdomain_tracking(domain)
		[line.strip() for line in ip_list]
		return ip_list
	except Exception as e:
		print ("   " + bad + "[ERROR]" + str(e))

def IPscan(domain, ns, A):
		url = 'http://' + domain
		if A != None:
			try:
				print (que + 'Using DIG to get the real IP')
				print ("   " + good + 'Possible IP: %s' % str(A))
				print(que + 'Retrieving target homepage at: %s' % url)
				try:
					org_response = requests.get(url, timeout=config['http_timeout_seconds'])
				except requests.exceptions.Timeout:
					sys.stderr.write("   " + bad + "%s timed out after %d seconds\n" % (url, config['http_timeout_seconds']))
				except requests.exceptions.RequestException:
					sys.stderr.write("   " + bad + "Failed to retrieve %s\n" % url)
				if org_response.status_code != 200:
					print ('   ' + bad + 'Responded with an unexpected HTTP status code')
				if org_response.url != url:
					print ('   ' + good + '%s redirects to %s' % (url, org_response.url))
					print ("   " + good + "Request redirected successful to %s" % org_response.url)
				try:
					sec_response = requests.get('http://' + str(A), timeout=config['http_timeout_seconds'])
					if sec_response.status_code != 200:
						print ('   ' + bad + 'Responded with an unexpected HTTP status code')
					else:
						page_similarity = similarity(sec_response.text, org_response.text)
						if page_similarity > config['response_similarity_threshold']:
							print (que + 'Testing if source body is the same in both websites')
							print ('   ' + good + ' HTML content is %d%% structurally similar to: %s' % (round(100 *page_similarity, 2), org_response.url))
				except Exception:
					print("   " + bad +"Connection Timeout")
				netcat(domain, ns, count=+1)
				return org_response
			except requests.exceptions.SSLError:
				print("   " + bad +'Error handshaking with SSL')
			except requests.exceptions.ReadTimeout:
				print("   " + bad +"Connection Timeout")
			except requests.ConnectTimeout:
				print("   " + bad +"Connection Timeout")