import random
from os import environ

import thirdparty.requests as requests
from thirdparty.dns.resolver import Resolver
from thirdparty.html_similarity import similarity

from ..utils.colors import Y, bad, good, info, tab
from ..utils.settings import config


def scan(domain, host, userAgent, randomAgent, header):
    headers = dict(x.replace(' ', '').split(':') for x in header.split(',')) if header is not None else {}
    (headers.update({'User-agent': random.choice(open("data/txt/random_agents.txt").readlines()).rstrip("\n")})
     if randomAgent is True else '')
    headers.update({'User-agent': userAgent}) if userAgent is not None else ''
    try:
        print("\n" + Y + "Attempting to track real IP using: %s\n" % host)
        print(info + "Checking if {0} is similar to {1}".format(host, domain))
        get_domain = requests.get('http://' + domain, headers=headers, timeout=config['http_timeout_seconds'])
        get_host = requests.get('http://' + host, headers=headers, timeout=config['http_timeout_seconds'])
        page_similarity = similarity(get_domain.text, get_host.text)
        if page_similarity > config['response_similarity_threshold']:
            print(tab + good + 'HTML content is %d%% structurally similar to: %s'
                  % (round(100 * page_similarity, 2), domain))
        else:
            print(tab + bad + 'Sorry, but HTML content is %d%% structurally similar to: %s'
                  % (round(100 * page_similarity, 2), domain))
    except Exception:
        print(tab + bad + 'Connection cannot be established with: %s' % (host))


def DNSLookup(domain, host):
    isAndroid = "ANDROID_DATA" in environ
    sys_r = Resolver(filename='/data/data/com.termux/files/usr/etc/resolv.conf') if isAndroid else Resolver()
    dns = [host]
    try:
        dream_dns = [item.address for server in dns for item in sys_r.query(server)]
        dream_r = Resolver()
        dream_r.nameservers = dream_dns
        answer = dream_r.query(domain, 'A')
        for A in answer.rrset.items:
            return A
    except Exception:
        pass
