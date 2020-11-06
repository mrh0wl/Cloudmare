import sys
from thirdparty.colorama import Fore, Style

if sys.platform.lower().startswith(('win32', 'darwin', 'ios', 'os')):
	W = Fore.WHITE
	G = Fore.GREEN
	R = Fore.RED
	Y = Fore.YELLOW
	B = Fore.BLUE
	end = Style.RESET_ALL
	info = Fore.YELLOW + '[!]' + Style.RESET_ALL
	que = Fore.BLUE + '[*]' + Style.RESET_ALL
	bad = Fore.RED + '[-]' + Style.RESET_ALL
	good = Fore.GREEN + '[+]' + Style.RESET_ALL
	run = Fore.WHITE + '[~]' + Style.RESET_ALL
	tab = "   "
else:
	W = '\033[97m'
	G = '\033[92m'
	R = '\033[91m'
	Y = '\033[93m'
	B = '\033[94m'
	end = '\033[0m'
	info = '\033[93m[!]\033[0m'
	que = '\033[94m[?]\033[0m'
	bad = '\033[91m[-]\033[0m'
	good = '\033[92m[+]\033[0m'
	run = '\033[97m[~]\033[0m'
	tab = "   "
