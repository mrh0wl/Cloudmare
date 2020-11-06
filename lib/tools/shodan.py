#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

try:
	from configparser import ConfigParser
except:
	from ConfigParser import ConfigParser


import thirdparty.requests as requests
import thirdparty.shodan.exception as ShodanException
from thirdparty.bs4 import BeautifulSoup
from lib.parse.settings import PYVERSION
from thirdparty.shodan import Shodan
from lib.parse.colors import bad, info, que, tab

def searchTitle(domain):
	html = requests.get('http://' + domain).text
	soup = BeautifulSoup(html, 'html.parser')
	title = soup.find('title').string
	return title

def shodan(domain, conf):
	title = searchTitle(domain)
	config = ConfigParser()
	config.read(conf)
	
	getAPI = config.get('SHODAN', 'API_KEY')
	if PYVERSION.startswith('3'):
		api_key = input(tab + info + 'Please enter your shodan API: ') if getAPI == '' else getAPI
	else:
		api_key = raw_input(tab + info + 'Please enter your shodan API: ') if getAPI == '' else getAPI
	if getAPI == '' or getAPI == '':
		question = input(tab + info + 'Do you want to save your shodan.io credentials? y/n: ') if PYVERSION.startswith('3') else raw_input(que + 'Do you want to save your shodan.io credentials? y/n: ')
		if question in ["yes", "y", "Y", "ye"]:
			config.set('SHODAN', 'API_KEY', api_key)
		with open('data/APIs/api.conf', 'w') as configfile:
			config.write(configfile)
	print(que + 'Enumerating historical data from: %s using Shodan.io' % domain)
	try:
		shodan = Shodan(api_key)
		banner = shodan.search_cursor('http.title:"%s"' % title)
		title_results = set([ip['ip_str'] for ip in banner])
		if title_results:
			return title_results
	except ShodanException.APITimeout as e:
		print(bad + "API timeout:" + str(e))
	except ShodanException.APIError as e:
		print(tab + bad + "Error with your shodan credentials: %s" % e)
