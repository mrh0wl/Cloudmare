import os
import sys
import json
import argparse
import configparser
from .api import SecurityTrails, SecurityTrailsError, SecurityTrailsTooManyRequests
from .api import SecurityTrailsForbidden


def main():
    parser = argparse.ArgumentParser(description='Query Security Trails')
    subparsers = parser.add_subparsers(help='Commands')
    parser_a = subparsers.add_parser('config', help='Configure pybinary edge')
    parser_a.add_argument('--key', '-k', help='Configure the API key')
    parser_a.set_defaults(which='config')
    parser_b = subparsers.add_parser('ip', help='Query an IP address')
    parser_b.add_argument('IP', help='IP to be requested')
    parser_b.set_defaults(which='ip')
    parser_c = subparsers.add_parser('ping', help='Check the SecurityTrails connection')
    parser_c.set_defaults(which='ping')
    parser_d = subparsers.add_parser('quota', help='Check your quota')
    parser_d.set_defaults(which='quota')
    parser_e = subparsers.add_parser('domain', help='Query information on a domain')
    parser_e.add_argument('DOMAIN', help='Domain to be requested')
    parser_e.add_argument('--subdomains', '-s', action='store_true',
            help='Get subdomains of this domain')
    parser_e.add_argument('--tags', '-t', action='store_true',
            help='Get tags related to this domain')
    parser_e.add_argument('--associated', '-a', action='store_true',
            help='Get domains associated with the given domain')
    parser_e.add_argument('--whois', '-w', action='store_true',
            help='Get whois information on a domain')
    parser_e.add_argument('--ips', '-i', action='store_true',
            help='Get passive DNS about an IP')
    parser_e.set_defaults(which='domain')
    parser_f = subparsers.add_parser('search', help='Search for a domain')
    parser_f.add_argument('FILTER', help='Domain to be requested', nargs='*')
    parser_f.add_argument('--stats', '-s', action='store_true', help='Only show stats')
    parser_f.set_defaults(which='search')
    args = parser.parse_args()

    configfile = os.path.expanduser('~/.config/securitytrails')

    if hasattr(args, 'which'):
        if args.which == 'config':
            if args.key:
                config = configparser.ConfigParser()
                config['SecurityTrails'] = {'key': args.key}
                with open(configfile, 'w') as cf:
                    config.write(cf)
            if os.path.isfile(configfile):
                print('In %s:' % configfile)
                with open(configfile, 'r') as cf:
                    print(cf.read())
            else:
                print('No configuration file, please use config --key')
        else:
            if not os.path.isfile(configfile):
                print('No configuration file, please use config --key')
                sys.exit(1)
            config = configparser.ConfigParser()
            config.read(configfile)
            try:
                st = SecurityTrails(config['SecurityTrails']['key'])
                if args.which == 'ip':
                    res = st.ips_search_stats(args.IP)
                    print(json.dumps(res, sort_keys=True, indent=4))
                elif args.which == 'domain':
                    if args.subdomains:
                        res = st.domain_subdomains(args.DOMAIN)
                        if "subdomains" in res:
                            for sd in res["subdomains"]:
                                print(sd)
                        else:
                            print('No subdomains found')
                    elif args.tags:
                        res = st.domain_tags(args.DOMAIN)
                        if "tags" in res:
                            if len(res['tags']):
                                for tag in res["tags"]:
                                    print(tag)
                            else:
                                print('No tags for this domain')
                        else:
                            print('No tags found')
                    elif args.ips:
                        res = st.domain_history_dns(args.DOMAIN)
                        print(json.dumps(res, sort_keys=True, indent=4))
                    elif args.associated:
                        res = st.domain_associated(args.DOMAIN)
                        print(json.dumps(res, sort_keys=True, indent=4))
                    elif args.whois:
                        res = st.domain_whois(args.DOMAIN)
                        print(json.dumps(res, sort_keys=True, indent=4))
                    else:
                        res = st.domain_info(args.DOMAIN)
                        print(json.dumps(res, sort_keys=True, indent=4))
                elif args.which == 'search':
                    filters = {}
                    for f in args.FILTER:
                        if '=' not in f:
                            print('Invalid argument {}, arguments should be like ipv4=8.8.8.8'.format(f))
                            sys.exit(1)
                        else:
                            ff = f.split('=')
                            if ff[0] not in st.SEARCH_FILTERS:
                                print('Invalid search filter')
                                print('Valid filters are: {}'.format(', '.join(st.SEARCH_FILTERS)))
                                sys.exit(1)
                            filters[ff[0]] = ff[1]
                    if args.stats:
                        res = st.domain_search(filters)
                        print(json.dumps(res, sort_keys=True, indent=4))
                    else:
                        res = st.domain_search_stats(filters)
                        print(json.dumps(res, sort_keys=True, indent=4))
                elif args.which == 'ping':
                    res = st.ping()
                    print(json.dumps(res, sort_keys=True, indent=4))
                elif args.which == 'quota':
                    res = st.usage()
                    print("Quota : {} / {}".format(
                            res['current_monthly_usage'],
                            res['allowed_monthly_usage']
                        )
                    )
                else:
                    print("Unknown command, please check help:")
                    parser.print_help()
            except SecurityTrailsForbidden as e:
                print('Forbidden: you need a more expensive plan for this request')
                sys.exit(1)
            except SecurityTrailsTooManyRequests as e:
                print('You have no more quota')
                sys.exit(1)
            except SecurityTrailsError as e:
                print('Error: {}'.format(e.message))
                sys.exit(1)
            except ValueError as e:
                print('Invalid Value: {}'.format(e.message))
                sys.exit(1)
    else:
        parser.print_help()
