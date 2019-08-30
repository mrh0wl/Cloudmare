#!/usr/bin/env python
# coding: utf-8
# By: MrH0wl

from __future__ import print_function
from __future__ import absolute_import

try:
	import os
	import sys 
	import thirdparty.requests as requests
	import thirdparty.urllib3 as urllib3
	from lib.parse.colors import white, green, red, yellow, end, info, que, bad, good, run
	from lib.parse.cmdline import parse_args, parse_error
	from lib.core.settings import osclear, quest, logotype, config
	from lib.tools.netcat import netcat
	from lib.tools.bruter import nameserver

except KeyboardInterrupt:
	quest(question=info + 'Are you sure you want to exit? y/n: ', doY="osclear(logotype = logotype(), unknown = bad + 'Sorry, but cannot clear this OS')", doN="pass")

try:
	import lxml
except ImportError:
	quest(question=(info + 'WARNING: A module is required. Do you want to install? y/n: '), doY = "pipmain(['install', 'lxml'])", doN = "sys.exit()")
from thirdparty.html_similarity import similarity
from lib.core.dnslookup import scan, DNSLookup
from thirdparty.dns.resolver import Resolver
from lib.core.subdomain_finder import subdomain_tracking

def make_list():
	ip_list = subdomain_tracking(domain)
	lst = [line.strip() for line in ip_list]
	return ip_list

def IPscan(domain):
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
			except requests.exceptions.RequestException as e:
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

if __name__=="__main__":
	try:
		args = parse_args()
		domain, file, brute = args.domain,args.file, args.bruter
		if args.subdomain == True and args.ns == None:
			ip_takes = make_list()
			if brute == True:
				nameservers = nameserver(domain)
				ip_takes.extend(nameservers)
			list_length = len(ip_takes)
			for i in range(0, list_length):
				ns = ip_takes[i]
				scan(domain, ns)
				netcat(domain, ns, count=0)
				A = DNSLookup(domain, ns)
				IPscan(domain)
		elif args.ns != None and args.subdomain == False:
			if brute == True:
				nameservers = nameserver(domain)
				nameservers.append(args.ns)
			list_length = len(nameservers) if brute is True else 1
			for i in range(0, list_length):
				ns = nameservers[i] if brute is True else args.ns
				scan(domain, ns)
				netcat(domain, ns, count=0)
				A = DNSLookup(domain, ns)
				IPscan(domain)
		else:
			parse_error(errmsg='too few arguments, please use "help" argument')
		if file != None:
			try:
				with open(file, 'w') as f:
					for ips in ns or ips in ip_takes:
						f.writelines(ips+"\n")
						if A != None:
							f.writelines(str(A)+"\n")
						print(info + 'Saved %d IP into output file %s' % (len([ips]), os.path.abspath(file)))
						if ips in ips:
							break
			except IOError as e:
				print('   '+ bad +'Unable to write to output file %s : %s\n' % (file, e))

	except KeyboardInterrupt:
		osclear(unknown= bad + "   " +"Sorry, but I cannot clear this OS")