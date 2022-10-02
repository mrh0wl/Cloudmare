#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

import sys

import thirdparty.shodan.exception as ShodanException
from thirdparty.shodan import Shodan

from ..utils.colors import bad, good, info, run, tab, warn
from .ispcheck import ISPCheck


def shodan(domain, conf):
    config = ConfigParser()
    config.read(conf)
    res = []
    getAPI = config.get('SHODAN', 'API_KEY')
    print(info + 'Enumerating data from: %s using Shodan.io' % domain)
    api_key = input(tab + warn + 'Please enter your shodan API: ') if getAPI == '' else getAPI
    if getAPI == '':
        question = input(tab + warn + 'Do you want to save your securitytrails credentials? [Y/n] ')
        if question in ["yes", "y", "Y", "ye", '']:
            config.set('SHODAN', 'API_KEY', api_key)
        with open(conf, 'w+') as configfile:
            config.write(configfile)
            configfile.close()
    try:
        shodan = Shodan(api_key)
        counts = shodan.count(query=domain, facets=['ip'])
        print(tab + warn + "Total Associated IPs Found:")
        [(print(tab*2 + good + ip['value']), res.append(ip['value'])) if (ISPCheck(ip['value']) is None)
         else print(tab * 2 + bad + ip['value'] + ISPCheck(ip['value'])) for ip in counts['facets']['ip']]
        return res
    except ShodanException.APITimeout as e:
        print(bad + "API timeout:" + str(e))
    except ShodanException.APIError as e:
        print(tab + bad + "Error with your shodan credentials: %s" % e)
        ans = input(tab + warn + "Do you want to delete your credentials? y/n: ")
        if ans in ["yes", "y", "Y", "ye"]:
            config.set('SHODAN', 'API_KEY', '')
            with open(conf, 'w+') as configfile:
                config.write(configfile)
            print(tab + good + "Your credentials have been deleted")
        print(tab + run + "Please re-run the script again")
        sys.exit()
