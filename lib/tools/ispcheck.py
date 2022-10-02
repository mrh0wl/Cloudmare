import re
import socket

from lib.utils.colors import R, W, Y, tab, warn
from thirdparty import requests
from thirdparty.bs4 import BeautifulSoup

cloudlist = ['sucuri',
             'cloudflare',
             'incapsula']


def ISPCheck(domain):
    reg = re.compile(rf'(?i){"|".join(cloudlist)}')
    try:
        header = requests.get('http://' + domain, timeout=1).headers['server'].lower()
        if reg.search(header):
            return f' is protected by {Y}{header.capitalize()}{W}'
        return None
    except Exception:
        req = requests.get(f'https://check-host.net/ip-info?host={domain}').text
        UrlHTML = BeautifulSoup(req, "lxml")
        print(f'{tab*2}{warn}Something has gone wrong. Retrying connection')
        if UrlHTML.findAll('div', {'class': 'error'}):
            return f' [{R}cannot retrieve information{W}]'

        for parse in UrlHTML.findAll('tr', {'class': 'zebra'}):
            if 'Organization' in str(parse):
                org = parse.get_text(strip=True).split('Organization')[1].lower()
                if reg.search(org):
                    return f' is protected by {Y}{reg.match(org).group().capitalize()}{W}'

        ports = [80, 443]

        for port in ports:
            checker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            checker.settimeout(0.5)
            if checker.connect_ex((domain, port)) == 0:
                checker.close()
                return
            checker.close()
            return f' [{R}http{W}/{R}https{W}] ports filtered or closed'
