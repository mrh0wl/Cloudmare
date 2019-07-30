#!/usr/bin/env python

from __future__ import absolute_import

import sys
from thirdparty.argparse import argparse
from lib.core.settings import logotype, COPYRIGHT, VERSION, NAME
from lib.parse.colors import white, green, red, yellow, end, info, que, bad, good, run

def parse_error(errmsg):
	logotype()
	print("Usage: python " + sys.argv[0] + " [Options] use -h for help")
	print(bad + errmsg)
	exit(1)

def parse_args():
	logotype()
	parser = argparse.ArgumentParser(epilog="\tExample: \r\npython " + sys.argv[0] + " [DOMAIN] -s")
	parser.error = parse_error
	parser._optionals.title = "OPTIONS"
	parser.add_argument("-v", '--version', action='version', version=NAME + VERSION + ' | '+ COPYRIGHT)
	parser.add_argument("domain", metavar="[domain]",help="domain to scan")
	parser.add_argument("-ns", "--nameserver", help="scan with nameserver", action='store', dest='ns', default=None)
	parser.add_argument("--subdomain", help="search misconfigured subdomain", action="store_true", default=False)
	return parser.parse_args()