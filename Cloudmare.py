#!/usr/bin/env python3
# coding: utf-8
# By: MrH0wl

# default imports
import re
import signal

from lib import (DNSLookup, IPscan, censys, logotype, nameserver, netcat,
                 parser_cmd, quest, scan, securitytrails, shodan, sublist3r)
from lib.tools import ISPCheck
from lib.utils.colors import bad, warn
from thirdparty import urllib3

urllib3.disable_warnings()
verify = False


def keyboard_exit(signum, frame):
    signal.signal(signal.SIGINT, original_sigint)

    quest(f"{warn}Do you want to clear the screen?", doY='osclear()', defaultAnswerFor='no')

    # restore the exit gracefully handler here
    signal.signal(signal.SIGINT, keyboard_exit)


if __name__ == "__main__":
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, keyboard_exit)
    args, parsErr = parser_cmd()
    output = "data/output/subdomains-from-" + (args.domain).split('.')[0] + ".txt" if args.outSub is None else False

    urlReg = re.compile(r'^(?:https?://)?(?:(?:w{2,3}\d{1})+|mobile\.|m(?:\d?)+\.)?((?:[.\w\d-]+))')
    args.domain = urlReg.search(args.domain).group(1)
    subdomain = sublist3r.main(args.domain, args.threads, output, ports=None,
                               silent=False, verbose=args.verbose,
                               enable_bruteforce=args.subbrute, engines=None) if not args.disableSub else []

    if len(subdomain) == 0 and not any((
            args.host,
            args.brute,
            args.subbrute,
            args.censys,
            args.shodan,
            args.securitytrails
    )
    ):
        logotype()
        parsErr("cannot continue with tasks. Add another argument to task (e.g. \"--host\", \"--bruter\")")
    if args.headers is not None and 'host:' in args.headers:
        logotype()
        parsErr("Remove the 'host:' header from the '--header' argument. Instead use '--host' argument")

    if args.host is not None:
        check = ISPCheck(args.host)
        subdomain.append(args.host) if check is None else print(f"{bad}{args.host}{check}")

    if args.brute is True:
        nameservers = nameserver(args.domain)
        subdomain.extend(nameservers)

    if args.censys is not None:
        CensysIP = censys(args.domain, args.censys)
        subdomain.extend(CensysIP)

    if args.shodan is not None:
        ShodanIP = shodan(args.domain, args.shodan)
        subdomain.extend(ShodanIP)

    if args.securitytrails is not None:
        STip = securitytrails(args.domain, args.securitytrails)
        subdomain.extend(STip)

    list_length = len(subdomain)
    for i in range(list_length):
        host = subdomain[i]
        scan(args.domain, host, args.uagent, args.randomAgent, args.headers)
        netcat(args.domain, host, args.ignoreRedirects, args.uagent, args.randomAgent, args.headers, count=0)
        A = DNSLookup(args.domain, host)
        IPscan(args.domain, host, A, args.uagent, args.randomAgent, args.headers, args)
