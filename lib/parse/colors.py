import sys
from thirdparty.colorama import Fore, Style, Back

if sys.platform.lower().startswith(('win32', 'darwin', 'ios', 'os')):
    white = Fore.WHITE
    green = Fore.GREEN
    red = Fore.RED
    yellow = Fore.YELLOW
    end = Style.RESET_ALL
    info = Fore.YELLOW + '[!]' + Style.RESET_ALL
    que = Fore.BLUE + '[*]' + Style.RESET_ALL
    bad = Fore.RED + '[-]' + Style.RESET_ALL
    good = Fore.GREEN + '[+]' + Style.RESET_ALL
    run = Fore.WHITE + '[~]' + Style.RESET_ALL
else:
    white = '\033[97m'
    green = '\033[92m'
    red = '\033[91m'
    yellow = '\033[93m'
    end = '\033[0m'
    info = '\033[93m[!]\033[0m'
    que = '\033[94m[?]\033[0m'
    bad = '\033[91m[-]\033[0m'
    good = '\033[92m[+]\033[0m'
    run = '\033[97m[~]\033[0m'
