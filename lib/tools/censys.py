import thirdparty.censys.ipv4
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
		c = thirdparty.censys.ipv4.CensysIPv4(api_id=ID, api_secret=SECRET)
		query = list(c.search('{0}'.format((domain)), ip, max_records=10))
		ip_data = [query[i]['ip'] for i in range(len(query))]
		print(tab + info + "Total Associated IPs Found:")
		if ip_data:
			ip = [(print(tab*2 + good + ip), censys_ip.append(ip)) if (ISPCheck(ip) == None) else print(tab *2 + bad + ip + ISPCheck(ip)) for ip in ip_data]
		return censys_ip
	except Exception as e:
		print(tab*2 + bad + str(e))