import thirdparty.requests as requests
from thirdparty.bs4 import BeautifulSoup
from thirdparty.censys.search import CensysHosts

from ..utils.colors import bad, good, info, tab, warn
from .ispcheck import ISPCheck

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser


def censys(domain, conf):
    config = ConfigParser()
    config.read(conf)
    censys_ip = []

    print(info + 'Enumerating historical data from: %s using Censys.io' % domain)
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
    req = requests.get('http://' + domain, headers=header)
    soup = BeautifulSoup(req.text, 'html.parser')
    title = soup.title.string if soup.title else None

    ID = (input(tab + warn + 'Please enter your censys ID: ') if config.get('CENSYS', 'API_ID') == ''
          else config.get('CENSYS', 'API_ID'))
    SECRET = (input(tab + warn + 'Now, please enter your censys SECRET: ') if config.get('CENSYS', 'SECRET') == ''
              else config.get('CENSYS', 'SECRET'))

    if config.get('CENSYS', 'API_ID') == '' or config.get('CENSYS', 'SECRET') == '':
        question = input(tab + warn + 'Do you want to save your securitytrails credentials? [Y/n] ')
        if question in ["yes", "y", "Y", "ye", '']:
            config.set('CENSYS', 'API_ID', ID)
            config.set('CENSYS', 'SECRET', SECRET)

        with open('data/APIs/api.conf', 'w') as configfile:
            config.write(configfile)
    try:
        c = CensysHosts(ID, SECRET)
        certificates = c.search("services.tls.certificates.leaf_data.subject.common_name: *.%s" % domain,
                                sort="RELEVANCE")
        search = certificates()
        if len(search) == 0:
            search = c.search("%s" % domain, sort="RELEVANCE")()
        if len(search) != 0:
            print(tab + warn + "Total IPs found using certificates with common names:")
        [(print(tab*2 + good + ip['ip']), censys_ip.append(ip['ip'])) if (ISPCheck(ip['ip']) is None)
         else print(tab * 2 + bad + ip['ip'] + ISPCheck(ip['ip'])) for ip in search]
        if title is not None:
            titles = c.search("services.http.response.html_title: '%s'" % title, sort="RELEVANCE")()
            if len(titles) != 0:
                print(tab + warn + "Total IPs found using HTML title:")
            [(print(tab*2 + good + ip['ip']), censys_ip.append(ip['ip'])) if (ISPCheck(ip['ip']) is None)
                else print(tab * 2 + bad + ip['ip'] + ISPCheck(ip['ip'])) for ip in titles]
        if len(censys_ip) == 0:
            print(tab + bad + "No IPs found using Censys.io")
        return censys_ip
    except Exception as e:
        print(tab*2 + bad + str(e))
