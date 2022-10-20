#!/usr/bin/env python3

'''
Copyright (c) 2018-2019 cloudmare developer
'''

from __future__ import absolute_import

import os
import sys

from .colors import G, R, W, Y, bad, end, good, tab, warn

''' try:
    from pip._internal import main as pip
except ImportError:
    print(bad + 'pip module not found...using \'ensurepip\' for solve the problem')
    subprocess.check_call([sys.executable, '-m', 'ensurepip']) '''

# enable VT100 emulation for coloR text output on windows platforms
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
VERSION = '2.2.10.1'
DESCRIPTION = 'Automatic CloudProxy and Reverse Proxy bypass tool'
ISSUES_PAGE = 'https://github.com/MrH0wl/Cloudmare/issues/new'
GIT_REPOSITORY = 'https://github.com/MrH0wl/Cloudmare.git'
GIT_PAGE = 'https://github.com/MrH0wl/Cloudmare'
ZIPBALL_PAGE = 'https://github.com/MrH0wl/Cloudmare/zipball/master'
YEAR = '2021'
NAME = 'Cloudmare '
COPYRIGHT = 'Copyright %s - GPL v3.0' % (YEAR)
PLATFORM = os.name
IS_WIN = PLATFORM == 'nt'

answers = {
    'affirmative': ['y', 'yes', 'ok', 'okay', 'sure', 'yep', 'yeah', 'yup', 'ya', 'yeh', 'ye', 'y'],
    'negative': ['n', 'no', 'nope', 'nop', 'naw', 'na', 'nah', 'nay', 'n'],
}


# colorful banner
def logotype():
    print(Y + '''
  ____ _                 _ __  __
 / ___| | ___  _   _  __| |  \\/  | __ _ _ __ ___
| |   | |/ _ \\| | | |/ _` | |\\/| |/ _` | '__/ _ \\
| |___| | (_) | |_| | (_| | |  | | (_| | | |  __/
 \\____|_|\\___/ \\__,_|\\__,_|_|  |_|\\__,_|_|  \\___| ''' + W + '[' + R + VERSION + W + ']' + '''
''' + G + DESCRIPTION + G + '\n##################################################' + W + '\n')


BASIC_HELP = (
    'domain',
    'bruter',
    'randomAgent',
    'host',
    'outSub',
)


# osclear shortcut
def osclear():
    if IS_WIN:
        os.system('cls')
    elif 'linux' in PLATFORM:
        os.system('clear')
    else:
        print("{bad} Can't identify OS")
    logotype()
    print(Y + '\n~ Thanks for using this script! <3')
    sys.exit(1)


def executer(command, **kwargs):
    try:
        if 'return' in kwargs.keys() and kwargs['return'] is True:
            return eval(command)
        exec(command)
    except Exception as e:
        if 'printError' in kwargs.keys():
            print(tab+kwargs['printError'])
            return
        print(f'{tab}{bad}{e}')


# question shortcut
def quest(question, doY='sys.exit(0)', doN='sys.exit(1)', defaultAnswerFor='yes', **kwargs):
    default = ' [Y/n]' if defaultAnswerFor.lower() in answers['affirmative'] else ' [y/N]'
    question = input(f'{question}{default}').lower().strip()

    if defaultAnswerFor.lower() == 'yes':
        answers['affirmative'].append('')
    elif defaultAnswerFor.lower() == 'no':
        answers['negative'].append('')

    if question in answers['affirmative']:
        exe = executer(doY, **kwargs)

    elif question in answers['negative']:
        exe = executer(doN, **kwargs)

    return exe


# Import Checker and downloader
class CheckImports:
    def __init__(self, libList=[]):
        for lib in libList:
            try:
                exec(lib)
            except ImportError or ModuleNotFoundError as e:
                if lib == libList[0]:
                    logotype()
                self.__downloadLib(e.name)

    def __downloadLib(self, lib):
        printMsg = {
            'printSuccess': f'{tab}{good}{lib} module is installed!',
            'printError': f'{tab}{bad}{lib} module is not installed! Try to install it manually.',
        }
        msg = f'{warn}{R}{lib}{end} module is required. Do you want to install?'
        command = f'subprocess.check_call([sys.executable, \'-m\', \'pip\', \'install\', \'{lib}\', '
        command += '\'--no-python-version-warning\', \'-q\', \'--disable-pip-version-check\'])'
        quest(question=msg, doY=f"import subprocess\n{command}\nprint(kwargs[\'printSuccess\'])",
              doN='continue', **printMsg)
