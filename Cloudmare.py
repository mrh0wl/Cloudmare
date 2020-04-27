#!/usr/bin/env python
# coding: utf-8
# By: MrH0wl

from __future__ import print_function
from __future__ import absolute_import

from lib.parse.settings import quest, logotype, osclear, config, checkImports
from lib.parse.colors import white, green, red, yellow, end, info, que, bad, good, run
import os, sys

while True:
	try:
		import thirdparty.requests as requests
		from lib.parse.cmdline import parse_args, parse_error
		from lib.core.ipscan import IPscan, make_list
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

if __name__=="__main__":
	try:
		args = parse_args()
		domain, file, brute, censysio = args.domain,args.file, args.bruter, args.censys
		if args.subdomain == True and args.ns == None:
			ip_takes = make_list(domain)
			if brute == True:
				nameservers = nameserver(domain)
				ip_takes.extend(nameservers)
			if censysio == True:
				CensysIP = censys(domain)
				ip_takes.extend(CensysIP)
			list_length = len(ip_takes)
			for i in range(0, list_length):
				ns = ip_takes[i]
				scan(domain, ns)
				netcat(domain, ns, count=0)
				A = DNSLookup(domain, ns)
				IPscan(domain, ns, A)
		elif args.ns != None and args.subdomain == False:
			if brute == True:
				nameservers = nameserver(domain)
				nameservers.append(args.ns)
			if censysio == True:
				CensysIP = censys(domain)
				ip_takes.extend(CensysIP)
			list_length = len(nameservers) if brute is True else 1
			for i in range(0, list_length):
				ns = nameservers[i] if brute is True else args.ns
				scan(domain, ns)
				netcat(domain, ns, count=0)
				A = DNSLookup(domain, ns)
				IPscan(domain, ns, A)
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
		question = input(info + '[INFO] Do you want to clear the screen? y/n: ') if sys.version_info[0] == 3 else raw_input(info + '[INFO] Do you want to clear the screen? y/n: ')
		if question in ["yes", "y", "Y", "ye"]:
			osclear(unknown= bad + "   " +"Sorry, but I cannot clear this OS")