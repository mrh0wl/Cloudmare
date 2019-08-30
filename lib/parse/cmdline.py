#!/usr/bin/env python

from __future__ import absolute_import

import sys
from thirdparty.argparse import argparse
from lib.core.settings import logotype, COPYRIGHT, VERSION, NAME
from lib.parse.colors import white, green, red, yellow, end, info, que, bad, good, run

def parse_error(errmsg):
	print("Usage: python " + sys.argv[0] + " [Options] use -h for help")
	print(bad + errmsg)
	exit(1)

def parse_args():
	logotype()
	formatter = lambda prog: argparse.HelpFormatter(prog,max_help_position=100)
	parser = argparse.ArgumentParser(epilog="\tExample: \r\npython " + sys.argv[0] + " [DOMAIN] --subdomain", formatter_class=formatter)
	parser.error = parse_error
	parser.add_argument("-v", '--version', action='version', version=NAME + VERSION + ' | '+ COPYRIGHT)
	parser.add_argument("domain", metavar="[domain]",help="domain to scan")
	group1 = parser.add_argument_group('PRIMARY OPTIONS', 'arguments necessary and useful')
	parser1 = group1.add_mutually_exclusive_group()
	parser1.add_argument("--subdomain", help="search misconfigured subdomain", action="store_true", default=False)
	parser1.add_argument("-ns", "--nameserver", metavar="ns", help="scan with nameserver", action='store', dest='ns', default=None)
	group2 = parser.add_argument_group('SECONDARY OPTIONS', 'arguments not necessary, but useful')
	parser2 = group2.add_mutually_exclusive_group()
	parser2.add_argument("-o","--output", metavar='out', help="save results in a file", dest='file', default=None)
	parser2.add_argument("--dns-bruter", help="bruteforce domain extensions", action="store_true", dest='bruter', default=False)
	return parser.parse_args()