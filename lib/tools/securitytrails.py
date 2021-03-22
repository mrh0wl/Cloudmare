#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
	from configparser import ConfigParser
except:
	from ConfigParser import ConfigParser

import sys
from lib.parse.settings import PYVERSION
from lib.parse.colors import bad, info, que, tab, good
from lib.analyzer.ispcheck import ISPCheck
from thirdparty.pysecuritytrails import SecurityTrails, SecurityTrailsError

def securitytrails(domain, conf):
	st_ip = []

	config = ConfigParser()
	config.read(conf)

	print(que + 'Enumerating historical data from: %s using SecurityTrails.com' % domain)
	if PYVERSION.startswith('3'):
		API_KEY = input(tab + info + 'Please enter your securitytrails API KEY: ') if config.get('SECURITYTRAILS', 'API_KEY') == '' else config.get('SECURITYTRAILS', 'API_KEY')
	else:
		API_KEY = raw_input(tab + info + 'Please enter your securitytrails API KEY: ') if config.get('SECURITYTRAILS', 'API_KEY') == '' else config.get('SECURITYTRAILS', 'API_KEY')

	if config.get('SECURITYTRAILS', 'API_KEY') == '' or config.get('SECURITYTRAILS', 'API_KEY') == '':
		question = input(tab + info + 'Do you want to save your securitytrails credentials? y/n: ') if PYVERSION.startswith('3') else raw_input(que + 'Do you want to save your securitytrails credentials? y/n: ')
		if question in ["yes", "y", "Y", "ye"]:
			config.set('SECURITYTRAILS', 'API_KEY', API_KEY)
		with open('data/APIs/api.conf', 'w') as configfile:
			config.write(configfile)
	
	st = SecurityTrails(API_KEY)

	try:
	    st.ping()
	except SecurityTrailsError:
	    print(tab*2 + bad + 'Ping failed. Check your connection or Try later.')
	    sys.exit(1)
	try:
		print(tab + info + "Total Historical DNS Found:")
		history_dns = [record["values"] for record in st.domain_history_dns(domain)["records"] if record["values"]]
		history_dns = [[(print(tab*2 + good + ip["ip"]), st_ip.append(ip["ip"])) if (ISPCheck(ip["ip"]) == None) else print(tab*2 + bad + ip["ip"] + ISPCheck(ip["ip"])) for ip in ip] for ip in history_dns]
	except Exception as e:
		print(tab*2 + bad + str(e))
	
	return st_ip