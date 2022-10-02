import random

import thirdparty.requests as requests
from thirdparty.html_similarity import similarity

from ..tools.netcat import netcat
from ..utils.colors import bad, good, info, tab
from ..utils.settings import config


def IPscan(domain, ns, A, userAgent, randomAgent, header, args):
    url = 'http://' + domain
    headers = dict(x.replace(' ', '').split(':') for x in header.split(',')) if header is not None else {}
    headers.update({
        'User-agent': (random.choice(open("data/txt/random_agents.txt")
                                     .readlines())
                       .rstrip("\n"))
    } if randomAgent is True else '')
    headers.update({'User-agent': userAgent}) if userAgent is not None else ''
    if A is not None:
        try:
            print(info + 'Using DIG to get the real IP')
            print(tab + good + 'Possible IP: %s' % str(A))
            print(info + 'Retrieving target homepage at: %s' % url)
            org_response = requests.get(url, headers=headers, timeout=config['http_timeout_seconds'])
            if org_response.status_code != 200:
                print(tab + bad + 'Responded with an unexpected HTTP status code')
            if org_response.url != url:
                print(tab + good + '%s Redirects to %s' % (url, org_response.url))
            try:
                sec_response = requests.get('http://' + str(A), headers=headers, timeout=config['http_timeout_seconds'])
                if sec_response.status_code != 200:
                    print(tab + bad + 'Responded with an unexpected HTTP status code')
                else:
                    page_similarity = similarity(sec_response.text, org_response.text)
                    if page_similarity > config['response_similarity_threshold']:
                        print(info + 'Testing if source body is the same in both websites')
                        print(tab + good + ' HTML content is %d%% structurally similar to: %s' %
                              (round(100*page_similarity, 2), org_response.url))
            except Exception:
                print(tab + bad + "Connection Timeout")
            netcat(domain, ns, args.ignoreRedirects, userAgent, randomAgent, args.headers, count=+1)
            return org_response
        except Exception:
            print(tab + bad + 'Connection error')
