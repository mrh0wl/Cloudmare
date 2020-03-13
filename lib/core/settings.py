#!/usr/bin/env python

"""
Copyright (c) 2018-2019 cloudmare developer
"""

from __future__ import absolute_import

import codecs
import os
import random
import re
import string
import sys

from lib.parse.colors import white, green, red, yellow, end, info, que, bad, good, run
from pip._internal import main as pip
import thirdparty.urllib3 as urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
config = {
	'http_timeout_seconds': 5,
	'response_similarity_threshold': 0.9
}

# version (<major>.<minor>.<month>.<day>)
VERSION = "1.8.3.13"
DESCRIPTION = "Automatic CloudProxy and reverse proxy bypass tool"
ISSUES_PAGE = "https://github.com/MrH0wl/Cloudmare/issues/new"
GIT_REPOSITORY = "https://github.com/MrH0wl/Cloudmare.git"
GIT_PAGE = "https://github.com/MrH0wl/Cloudmare"
ZIPBALL_PAGE = "https://github.com/MrH0wl/Cloudmare/zipball/master"
YEAR = '2020'
NAME = 'Cloudmare '
COPYRIGHT = "Copyright %s - GPL v3.0"%(YEAR)

# colorful banner
def logotype():
	print (yellow + '''
  ____ _                 _ __  __
 / ___| | ___  _   _  __| |  \/  | __ _ _ __ ___
| |   | |/ _ \| | | |/ _` | |\/| |/ _` | '__/ _ \\
| |___| | (_) | |_| | (_| | |  | | (_| | | |  __/
 \____|_|\___/ \__,_|\__,_|_|  |_|\__,_|_|  \___| '''+ white + '[' + red + VERSION + white + ']' +'''
''' + green + DESCRIPTION + green + "\n##################################################"+ white + '\n')

# osclear shortcut
def osclear(unknown):
	isOs = sys.platform.lower()
	if 'win32' in isOs:
		os.system('cls')
	elif 'linux' in isOs:
		os.system('clear')
	else:
	  print(unknown)
	  sys.exit()
	logotype()
	print (yellow + "\n~ Thanks for using this script! <3")

# question shortcut
def quest(question, doY, doN, exportVar = None):
	end = ''
	try:
		isPy = sys.version_info[0]
		if isPy == 3:
			question = input(question)
		else:
			question = raw_input(question)
		if question == 'yes' or question == 'y':
			try: 
				exec(doY)
			except KeyboardInterrupt:
				sys.exit()
		elif question == 'no' or question == 'n':
			exec(doN)
		else:
			exec(doY)
		if end == None:
			pass
		else:
			print(end)
		
	except KeyboardInterrupt:
		sys.exit()

#Import Checker and downloader
class checkImports:
	def __init__(self, lib):
		self.lib = lib
		self.errlist = []

	def downloadLib(self, imports):
		self.errlist.append(self.lib)
		for i in self.errlist:
			if i in self.errlist:
				quest(question=(info + 'WARNING: ' + red + i + end + ' module is required. Do you want to install? y/n: '), exportVar = i, doY = "pip(['install', exportVar, '--no-python-version-warning', '-q', '--disable-pip-version-check', '--no-warn-conflicts', '--no-warn-script-location']) and sys.exit()", doN = "sys.exit()")
				