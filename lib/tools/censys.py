import sys
import thirdparty.censys
import thirdparty.censys.ipv4
import thirdparty.censys.certificates

from lib.parse.colors import white, green, red, yellow, end, info, que, bad, good, run

ID = None
SECRET = None

if sys.version_info[0] == 3:
    ID = input(info + 'Please enter your censys ID: ')
    SECRET = input(info + 'Now, please enter your censys SECRET: ')

else:
    ID = raw_input(info + 'Please enter your censys ID: ')
    SECRET = raw_input(info + 'Now, please enter your censys SECRET: ')

