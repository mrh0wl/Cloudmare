#!/usr/bin/env python3
# coding: utf-8
# By: MrH0wl

from __future__ import print_function
from __future__ import absolute_import

import sys
from lib.parse.cmdline import parser_cmd
from lib.parse.settings import logotype, osclear, checkImports, PYVERSION
from lib.parse.colors import info, bad

while True:
	try:
		from lib.analyzer.ipscan import IPscan
		from lib.analyzer.dnslookup import scan, DNSLookup
		from lib.tools import sublist3r
		from lib.tools.netcat import netcat
		from lib.tools.bruter import nameserver
		from lib.tools.censys import censys
		from lib.tools.shodan import shodan
		break
	except Exception as e:
		err = e.name if PYVERSION.startswith('3') else str(e).split('named')[1]
		checkImports(err).downloadLib()


if __name__=="__main__":
	try:
		args, parsErr = parser_cmd()
		output = "data/output/subdomains-from-" + (args.domain).split('.')[0] + ".txt" if args.outSub == None else False

		if args.disableSub == False:
			args.subbrute = False
			subdomain = sublist3r.main(args.domain, args.threads, output, ports=None, silent=False, verbose=args.verbose, enable_bruteforce=args.subbrute, engines=None)
			if len(subdomain) == 0 and not any((args.host, args.brute, args.subbrute, args.censys, args.shodan)):
				logotype()
				parsErr("cannot continue with tasks. Add another argument to task (e.g. \"--host\", \"--bruter\"")
		else: 
			subdomain = []
		if args.headers != None and 'host:' in args.headers:
			logotype()
			parsErr("Remove the 'host:' header from the '--header' argument. Instead use '--host' argument")

		if args.host != None:
			nameservers = []
			if args.brute == True:
				nameservers = nameserver(args.domain)
				nameservers.append(args.host)
			if args.censys != None:
				CensysIP = censys(args.domain, args.censys)
				subdomain.extend(CensysIP)
			if args.shodan != None:
				ShodanIP = shodan(args.domain, args.shodan)
				subdomain.extend(ShodanIP)
			list_length = len(nameservers) if args.brute == True else 1
			for i in range(0, list_length):
				host = nameservers[i] if args.brute == True else args.host
				scan(args.domain, host, args.uagent, args.randomAgent, args.headers)
				netcat(args.domain, host, args.ignoreRedirects, args.uagent, args.randomAgent, args.headers, count=0)
				A = DNSLookup(args.domain, host)
				IPscan(args.domain, host, A, args.uagent, args.randomAgent, args.headers, args)
		else:
			if args.brute == True:
				nameservers = nameserver(args.domain)
				subdomain.extend(nameservers)
			if args.censys != None:
				CensysIP = censys(args.domain, args.censys)
				subdomain.extend(CensysIP)
			if args.shodan != None:
				ShodanIP = shodan(args.domain, args.shodan)
				subdomain.extend(ShodanIP)
			list_length = len(subdomain)
			for i in range(0, list_length):
				host = subdomain[i]
				scan(args.domain, host, args.uagent, args.randomAgent, args.headers)
				netcat(args.domain, host, args.ignoreRedirects, args.uagent, args.randomAgent, args.headers, count=0)
				A = DNSLookup(args.domain, host)
				IPscan(args.domain, host, A, args.uagent, args.randomAgent, args.headers, args)
	except KeyboardInterrupt:
		question = input('\n' + info + 'Do you want to clear the screen? y/n: ') if sys.version_info[0] == 3 else raw_input(info + '[INFO] Do you want to clear the screen? y/n: ')
		if question in ["yes", "y", "Y", "ye"]:
			osclear(unknown= bad + "   " +" Sorry, but I cannot clear this OS")
