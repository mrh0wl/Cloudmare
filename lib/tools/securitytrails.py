#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

from thirdparty.pysecuritytrails import SecurityTrails, SecurityTrailsError

from ..utils.colors import W, Y, bad, good, info, tab, warn
from .ispcheck import ISPCheck


def securitytrails(domain, conf):
    config = ConfigParser()
    config.read(conf)
    st_ip = []

    print(info + 'Enumerating historical data from: %s using SecurityTrails.com' % domain)
    API_KEY = (input(tab + warn + 'Please enter your securitytrails API KEY: ')
               if config.get('SECURITYTRAILS', 'API_KEY') == ''
               else config.get('SECURITYTRAILS', 'API_KEY')
               )

    if config.get('SECURITYTRAILS', 'API_KEY') == '' or config.get('SECURITYTRAILS', 'API_KEY') == '':
        question = input(tab + warn + 'Do you want to save your securitytrails credentials? [Y/n] ')
        if question in ["yes", "y", "Y", "ye", '']:
            config.set('SECURITYTRAILS', 'API_KEY', API_KEY)
        with open('data/APIs/api.conf', 'w') as configfile:
            config.write(configfile)

    st = SecurityTrails(API_KEY)
    print(tab + warn + "Total Historical DNS Found:")
    try:
        views = []
        history_dns = [record["values"] for record in st.domain_history_dns(domain)["records"] if record["values"]]
        for ips in history_dns:
            for ip in ips:
                if ip['ip'] in views:
                    continue
                views.append(ip['ip'])
                ispValid = ISPCheck(ip["ip"]) is None
                if (ispValid):
                    print(tab*2 + good + ip["ip"])
                    st_ip.append(ip["ip"])
                    continue
                print(tab*2 + bad + ip["ip"] + ISPCheck(ip["ip"]))

        return st_ip
    except SecurityTrailsError as e:
        print(f'{tab*2}{bad}{e.message.split(":")[1].strip()}: {Y}https://securitytrails.com/app/plans/change{W}')
        return []
