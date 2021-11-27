#!/usr/bin/env python

"""
Copyright (c) 2018-2019 cloudmare developer
"""

from __future__ import absolute_import

import os
import sys
import subprocess
from lib.parse.colors import W, G, R, Y, end, info, tab, good, bad
try:
	from pip._internal import main as pip
except ImportError:
    print(bad + "pip module not found...using 'ensurepip' for solve the problem")
    subprocess.check_call([sys.executable, "-m", "ensurepip"])

#enable VT100 emulation for coloR text output on windows platforms
if sys.platform.startswith('win'):
	import ctypes
	kernel32 = ctypes.WinDLL('kernel32')
	hStdOut = kernel32.GetStdHandle(-11)
	mode = ctypes.c_ulong()
	kernel32.GetConsoleMode(hStdOut, ctypes.byref(mode))
	mode.value |= 4
	kernel32.SetConsoleMode(hStdOut, mode)


config = {
	'http_timeout_seconds': 5,
	'response_similarity_threshold': 0.9
}

# version (<major>.<minor>.<month>.<day>)
VERSION = "2.1.10.11"
DESCRIPTION = "Automatic CloudProxy and Reverse Proxy bypass tool"
ISSUES_PAGE = "https://github.com/MrH0wl/Cloudmare/issues/new"
GIT_REPOSITORY = "https://github.com/MrH0wl/Cloudmare.git"
GIT_PAGE = "https://github.com/MrH0wl/Cloudmare"
ZIPBALL_PAGE = "https://github.com/MrH0wl/Cloudmare/zipball/master"
YEAR = '2021'
NAME = 'Cloudmare '
COPYRIGHT = "Copyright %s - GPL v3.0"%(YEAR)
PLATFORM = os.name
PYVERSION = sys.version.split()[0]
IS_WIN = PLATFORM == "nt"

# colorful banner
def logotype():
	print (Y + '''
  ____ _                 _ __  __
 / ___| | ___  _   _  __| |  \/  | __ _ _ __ ___
| |   | |/ _ \| | | |/ _` | |\/| |/ _` | '__/ _ \\
| |___| | (_) | |_| | (_| | |  | | (_| | | |  __/
 \____|_|\___/ \__,_|\__,_|_|  |_|\__,_|_|  \___| '''+ W + '[' + R + VERSION + W + ']' +'''
''' + G + DESCRIPTION + G + "\n##################################################"+ W + '\n')

BASIC_HELP = (
    "domain",
    "bruter",
    "randomAgent",
    "host",
    "outSub",
)

# osclear shortcut
def osclear(unknown):
	if IS_WIN:
		os.system('cls')
	elif 'linux' in PLATFORM:
		os.system('clear')
	else:
	  print(unknown)
	  sys.exit()
	logotype()
	print (Y + "\n~ Thanks for using this script! <3")

# question shortcut
def quest(question, doY, doN, exportVar = None):
	end = ''
	try:
		if '3' in PYVERSION:
			question = input(question)
		else:
			question = raw_input(question)
		if question == 'yes' or question == 'y':
			try: 
				exec(doY)
			except KeyboardInterrupt:
				sys.exit()
			except Exception as er:
				print (tab + bad + 'An unexpected error has ocurred: %s' % (er))
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

	def downloadLib(self):
		self.errlist.append(self.lib)
		for i in self.errlist:
			if i in self.errlist:
				if PYVERSION.startswith('3'):
					quest(question=(info + 'WARNING: ' + R + i + end + ' module is required. Do you want to install? y/n: '), exportVar = i, doY = "subprocess.check_call([sys.executable, '-m', 'pip', 'install', exportVar, '--no-python-version-warning', '-q', '--disable-pip-version-check'])", doN = "sys.exit()")
					print(tab + good + '%s module installed sucessfully' % i)
				else:
					quest(question=(info + 'WARNING: ' + R + i + end + ' module is required. Do you want to install? y/n: '), exportVar = i, doY = "pip(['install', exportVar, '--no-python-version-warning', '-q', '--disable-pip-version-check', '--no-warn-conflicts', '--no-warn-script-location']) and sys.exit()", doN = "sys.exit()")
					print(tab + good + '%s module installed sucessfully' % i)
