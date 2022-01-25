import requests
from bs4 import BeautifulSoup
from thirdparty.censys.search import CensysHosts
from lib.parse.colors import info, que, bad, good, tab
from lib.parse.settings import PYVERSION
from lib.analyzer.ispcheck import ISPCheck
try:
	from configparser import ConfigParser
except:
	from ConfigParser import ConfigParser

def censys(domain, conf):
	config = ConfigParser()
	config.read(conf)
	censys_ip = []

	print(que + 'Enumerating historical data from: %s using Censys.io' % domain)
	req = requests.get('http://' + domain, allow_redirects=True)
	soup = BeautifulSoup(req.text, 'html.parser')
	title = soup.title.string if soup.title else None
	if PYVERSION.startswith('3'):
		ID = input(tab + info + 'Please enter your censys ID: ') if config.get('CENSYS', 'API_ID') == '' else config.get('CENSYS', 'API_ID')
		SECRET = input(tab + info + 'Now, please enter your censys SECRET: ') if config.get('CENSYS', 'SECRET') == '' else config.get('CENSYS', 'SECRET')

	else:
		ID = raw_input(tab + info + 'Please enter your censys ID: ') if config.get('CENSYS', 'API_ID') == '' else config.get('CENSYS', 'API_ID')
		SECRET = raw_input(tab + info + 'Now, please enter your censys SECRET: ') if config.get('CENSYS', 'SECRET') == '' else config.get('CENSYS', 'SECRET')

	if config.get('CENSYS', 'API_ID') == '' or config.get('CENSYS', 'SECRET') == '':
		question = input(tab + info + 'Do you want to save your censys.io credentials? y/n: ') if PYVERSION.startswith('3') else raw_input(que + 'Do you want to save your censys.io credentials? y/n: ')
		if question in ["yes", "y", "Y", "ye"]:
			config.set('CENSYS', 'API_ID', ID)
			config.set('CENSYS', 'SECRET', SECRET)

		with open('data/APIs/api.conf', 'w') as configfile:
			config.write(configfile)
	try:
		ip = ['ip']
		c = CensysHosts(ID, SECRET)
		certificates = c.search("services.tls.certificates.leaf_data.subject.common_name: *.%s" % domain, sort="RELEVANCE")
		print(tab + info + "Total IPs found using certificates with common names:")
		ip = [(print(tab*2 + good + ip['ip']), censys_ip.append(ip['ip'])) if (ISPCheck(ip['ip']) == None) else print(tab *2 + bad + ip['ip'] + ISPCheck(ip['ip'])) for ip in certificates()]
		if title != None:
			titles = c.search("services.http.response.html_title: '%s'" % title, sort="RELEVANCE")
			print(tab + info + "Total IPs found using HTML title:")
			title_ip = [(print(tab*2 + good + ip['ip']), censys_ip.append(ip['ip'])) if (ISPCheck(ip['ip']) == None) else print(tab *2 + bad + ip['ip'] + ISPCheck(ip['ip'])) for ip in titles()]
		return censys_ip
	except Exception as e:
		print(tab*2 + bad + str(e))