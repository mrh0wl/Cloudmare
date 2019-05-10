#!/usr/bin/env python
# coding: utf-8
# Cloudmare v1.4
# By Secmare - twitter.com/secmare

import os
import sys
import socket
import colorama
import requests
import urllib3
import dns
import dns.resolver
import dns.exception
import argparse

from dnsdumpster.DNSDumpsterAPI import DNSDumpsterAPI
from html_similarity import similarity
from dns.resolver import Resolver
from colorama import Fore, Style, Back

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
colorama.init(autoreset=True)
config = {
	'http_timeout_seconds': 3,
	'response_similarity_threshold': 0.9
}

def logotype():
	print Fore.YELLOW + '''\
  ____ _                 _ __  __
 / ___| | ___  _   _  __| |  \/  | __ _ _ __ ___
| |   | |/ _ \| | | |/ _` | |\/| |/ _` | '__/ _ \
| |___| | (_) | |_| | (_| | |  | | (_| | | |  __/
 \____|_|\___/ \__,_|\__,_|_|  |_|\__,_|_|  \___|
	''' + Fore.RESET + Style.DIM + Fore.WHITE + '''
 ================================================
 ||                  Secmare                   ||
 ||            twitter.com/secmare             ||
 ||                  v1.4.56                   ||
 ================================================
	''' + Fore.RESET


def parse_error(errmsg):
	logotype()
	print("Usage: python " + sys.argv[0] + " [Options] use -h for help")
	print(Fore.RED + "[-] " + Fore.RESET + errmsg)
	exit(1)

def parse_args():
	parser = argparse.ArgumentParser(epilog="\tExample: \r\npython " + sys.argv[0] + " [DOMAIN] -s -o output.txt")
	parser.error = parse_error
	parser._optionals.title = "OPTIONS"
	parser.add_argument("-v", '--version', action='version', version='%(prog)s 1.4.56 | Copyright 2018 - GPL v3.0')
	parser.add_argument("domain", metavar="[domain]",help="The domain to scan")
	parser.add_argument("-s", "--subdomain", help="Scan for subdomain misconfigured", action="store_true", default=False)
	parser.add_argument("-ns", "--nameserver", help="Scan using your obtained NameServer", action='store', dest='ns', default=None)
	return parser.parse_args()



def put_file():
	line = open('vulnsubdomain.txt', 'r+')
	file = line.readline().replace("\n", "")
	line.close
	return file

def subdomain_tracking(domain):
	print (Fore.YELLOW + Style.BRIGHT + "Tracking subdomains and MX records...\n")
	ip_takes = []
	res = DNSDumpsterAPI(False).search(domain)
	if res['dns_records']['host']:
		print (Fore.BLUE + "[*] " + Fore.RESET + "Subdomains:")
		for entry in res['dns_records']['host']:
			print (Fore.GREEN + "   [+] " + Fore.RESET + "{ip}".format(**entry) + " from: " + "{domain}".format(**entry))
	if res['dns_records']['mx']:
		print (Fore.BLUE + "[*] " + Fore.RESET + "MX Records:")
		for entry in res['dns_records']['mx']:
			print (Fore.GREEN + "   [+] " + Fore.RESET + "{ip}".format(**entry) + " from: " + "{domain}".format(**entry))
	print(Fore.BLUE + "\n[*]" + Fore.RESET + "Enumerating misconfigured DNS subdomains:")

	try:
		for entry in res['dns_records']['host']:
			provider = str(entry['provider'])
			ip = str(entry['ip'])
			if "Cloudflare" not in provider and ip not in ip:
				ip_takes.append('{ip}'.format(**entry))
				print (Fore.GREEN + "   [+] " + Fore.RESET + "{ip}".format(**entry) + " from: " + "{domain}".format(**entry))
		for entry in res['dns_records']['mx']:
			provider = str(entry['provider'])
			ip = str(entry['ip'])
			if "Cloudflare" not in provider and ip not in ip_takes:
				ip_takes.append('{ip}'.format(**entry))
				print (Fore.GREEN + "   [+] " + Fore.RESET + "{ip}".format(**entry) + " from: " + "{domain}".format(**entry))
	except:
		print(Fore.RED + "   [-]" + Fore.RESET + " All IPs belong to the Cloudflare Network")
		exit(1)
	if ip_takes != None:
		with open('vulnsubdomain.txt', 'w+') as file:
			ip_takes = map(str, ip_takes)
			line = "\n".join(ip_takes)
			file.write(line)
			file.close()


def first_scan():
	try:
		print(Fore.YELLOW + Style.BRIGHT +"Cloudflare IP Catcher (Auto DIG)...\n")
		print(Fore.BLUE + "[*]" + Fore.RESET + " Checking if {0} are similar to {1}".format(ns, domain))
		test1 = requests.get('http://' + domain, timeout=config['http_timeout_seconds'])
		test2 = requests.get('http://' + ns, timeout=config['http_timeout_seconds'])
		page_similarity2 = similarity(test1.text, test2.text)
		if page_similarity2 > config['response_similarity_threshold']:
			print (((Fore.GREEN + '   [+]' + Fore.RESET) + ' HTML content is %d%% structurally similar to: %s' % (round(100 *page_similarity2, 2), domain)))
		else:
			print (((Fore.RED + '   [-]' + Fore.RESET + ' Sorry, but HTML content is %d%% structurally similar to %s' % (round(100 *page_similarity2, 2), domain))))
			print ("\n - Trying to check with IP... \n")
	except requests.exceptions.Timeout:
		sys.stderr.write((Fore.RED + "   [-]" + Fore.RESET) + " Connection cannot be established... Try to put manually a NS\n")
		exit(1)
	except requests.exceptions.Timeout:
		sys.stderr.write((Fore.RED + "   [-]" + Fore.RESET) + " Connection cannot be established... Try to put manually a NS\n")
		exit(1)


def first_nc(domain):
	ip = socket.gethostbyname(ns)
	url = 'http://' + domain
	page = requests.get(url, timeout=config['http_timeout_seconds'])
	hncat = page.url.replace('https://www.', '').split('/')[0]
	home = page.url.replace('https://', '').split('.')[-2]
	print ((Fore.BLUE + '[*]' + Fore.RESET + ' Testing if are the real IP'))
	data = "GET /{0} HTTP/1.1\r\nHost: {1}\r\n\r\n".format(home, hncat)

	client = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
	client.connect(( ip, 80 ))
	client.sendall(data)
	response = client.recv(2048)
	if '200 OK' in response:
		print ((Fore.GREEN + "   [+]" + Fore.RESET) + " The Real IP is: %s." % ip)
		exit(1)
	if '301' in response:
		print ((Fore.GREEN + "   [+]" + Fore.RESET) + " The Real IP is: %s." % ip)
		exit(1)
	else:
		print ((Fore.RED + "   [-]" + Fore.RESET) + " %s is not the IP." %ip)
		print ((Fore.BLUE + '[*]' + Fore.RESET) + ' Trying to DIG for obtain the Real IP')

def Checking_DNS(ns, dns):
	try:
		dream_dns = [item.address for server in dns for item in sys_r.query(server)]
		dream_r = Resolver()
		dream_r.nameservers = dream_dns
		answer = dream_r.query(domain, 'A')
		for A in answer.rrset.items:
			A
	except:
		print (Fore.RED + '   [-]' + Fore.RESET) + ' IP not found.'
		print ("\n - Exiting...")
		exit(1)
	return A

def Checking_IP(domain):
	A = Checking_DNS(ns, dns)
	print (Fore.GREEN + '   [+]' + Fore.RESET) + ' Possible IP:', A
	url = 'http://' + domain
	print((Fore.BLUE + '[*]') + Fore.RESET + ' Retrieving target homepage at: %s' % url)
	try:
		org_response = requests.get(url, timeout=config['http_timeout_seconds'])
	except requests.exceptions.Timeout:
		sys.stderr.write((Fore.RED + "   [-]" + Fore.RESET) + " %s timed out after %d seconds.\n" % (url, config['http_timeout_seconds']))
		exit(1)
	except requests.exceptions.RequestException as e:
		sys.stderr.write((Fore.RED + "   [-]" + Fore.RESET) + " Failed to retrieve %s.\n" % url)
		exit(1)

	if org_response.status_code != 200:
		print (Fore.RED + '   [-]' + Fore.RESET) + ' %s responded with an unexpected HTTP status code %d' % (url, org_response.status_code)
		exit(1)

	if org_response.url != url:
		print ((Fore.GREEN + '[+]' + Fore.RESET) + ' %s redirects to %s.' % (url, org_response.url))
		print (Fore.GREEN + "   [+]" + Fore.RESET + " Request redirected successful to %s." % org_response.url)
	print ((Fore.BLUE + '[*]' + Fore.RESET + ' Testing if body content is the same in both websites.'))

	sec_response = requests.get('http://' + str(A), timeout=config['http_timeout_seconds'])
	if sec_response.status_code != 200:
		print (Fore.RED + '   [-]' + Fore.RESET) + ' %s responded with an unexpected HTTP status code %d' % (url, org_response.status_code)
		exit(1)
	if sec_response.text == org_response.text:
		print ((str(A), 'HTML content identical to %s' % domain))
	page_similarity = similarity(sec_response.text, org_response.text)
	if page_similarity > config['response_similarity_threshold']:
		print (((Fore.GREEN + '   [+]' + Fore.RESET) + ' HTML content is %d%% structurally similar to: %s' % (round(100 *page_similarity, 2), org_response.url)))
	return org_response

def second_nc(domain):
	A = Checking_DNS(ns, dns)
	ip = str(A)
	url = 'http://' + domain
	page = requests.get(url, timeout=config['http_timeout_seconds'])
	hncat = page.url.replace('https://www.', '').split('/')[0]
	home = page.url.replace('https://', '').split('.')[-2]
	print ((Fore.BLUE + '[*]' + Fore.RESET + ' Testing if are the real IP'))
	data = "GET /{0} HTTP/1.1\r\nHost: {1}\r\n\r\n".format(home, hncat)

	client = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
	client.connect(( ip, 80 ))
	client.sendall(data)
	response = client.recv(2048)
	if '200 OK' in response:
		print ((Fore.GREEN + "   [+]" + Fore.RESET) + " The Real IP is: %s." % ip)
		exit(1)
	if '301' in response:
		print ((Fore.GREEN + "   [+]" + Fore.RESET) + " The Real IP is: %s." % ip)
		exit(1)
	else:
		print ((Fore.RED + "   [-]" + Fore.RESET) + " %s is not the IP." %ip)

if __name__=="__main__":
	try:
		args = parse_args()
		sys_r = Resolver()
		domain = args.domain
		if args.subdomain == True:
			logotype()
			subdomain_tracking(domain)
			ns = put_file()
		elif args.ns != None:
			ns = args.ns
			logotype()
		else:
			logotype()
			print("Usage: python " + sys.argv[0] + " [Options] use -h for help")
			print ((Fore.RED + "[-]" + Fore.RESET) + " too few arguments")
			exit(0)

		dns = [ns]
		first_scan()
		first_nc(domain)
		Checking_DNS(ns, dns)
		Checking_IP(domain)
		second_nc(domain)
	except KeyboardInterrupt:
		print ("\n" * 80)
		os.system('clear')
		logotype()
		print(Fore.YELLOW + " ~ Thanks to use this script! <3")
		sys.exit(0)
	except Exception as e:
		str(e)
		sys.stderr.write((Fore.RED + "   [-]" + Fore.RESET) + " Connection cannot be established... Try to put manually a NS\n")
		exit(1)
