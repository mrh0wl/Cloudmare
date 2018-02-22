#!/usr/bin/env python
# coding: utf-8
# Cloudmare v1.0
# By Secmare - twitter.com/secmare 

import sys
import socket
import colorama
import requests
import urllib3
import dns.resolver
import dns.exception
import argparse

from html_similarity import similarity
from dns.resolver import Resolver
from colorama import Fore, Style, Back

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
colorama.init(autoreset=True)
config = {
    'http_timeout_seconds': 3,
    'response_similarity_threshold': 0.9
}
logo = '''\
  ____ _                 _ __  __                
 / ___| | ___  _   _  __| |  \/  | __ _ _ __ ___ 
| |   | |/ _ \| | | |/ _` | |\/| |/ _` | '__/ _ \                  
| |___| | (_) | |_| | (_| | |  | | (_| | | |  __/
 \____|_|\___/ \__,_|\__,_|_|  |_|\__,_|_|  \___|
 '''

logo2 ='''
 ================================================
 ||                  Secmare                   ||
 ||            twitter.com/secmare             ||
 ||                   v1.0                     ||
 ================================================
'''
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("target", metavar="[domain]",help="The domain to scan.")
parser.add_argument("-s", dest='subdomain', default="None", help="Server to compare with target.")
parser.add_argument("-v", '--version', action='version', version='%(prog)s 1.0 | Copyright 2018 - GPL v3.0')
args = parser.parse_args()
hostname = args.target
server_name = args.subdomain

print(Fore.YELLOW + logo), (Style.DIM + Fore.WHITE + logo2)

sys_r = Resolver()

print(Fore.YELLOW + Style.BRIGHT +"Cloudflare IP Catcher (Auto DIG)...")

domain = hostname
port = 80
ns = server_name
dns = [ns]
print(Fore.BLUE + "[*]" + Fore.RESET + " Checking if {0} are similar to {1}...".format(ns, domain))
test1 = requests.get('http://' + domain, timeout=config['http_timeout_seconds'])
test2 = requests.get('http://' + ns, timeout=config['http_timeout_seconds'])
page_similarity2 = similarity(test1.text, test2.text)
if page_similarity2 > config['response_similarity_threshold']:
	print (((Fore.GREEN + '[+]' + Fore.RESET) + ' HTML content is %d%% structurally similar to: %s' % (round(100 *page_similarity2, 2), domain)))
else:
	print (((Fore.RED + '[-]' + Fore.RESET + ' Sorry, but HTML content is %d%% structurally similar to %s' % (round(100 *page_similarity2, 2), domain))))
	print ("\n - Trying to check with IP... \n")

def netcat(domain):
	ip = socket.gethostbyname(ns)
	url = 'http://' + domain
	page = requests.get(url, timeout=config['http_timeout_seconds'])
	hncat = page.url.replace('https://www.', '').split('/')[0]
	home = page.url.replace('https://', '').split('.')[-2]
	home2 = home.replace('com', '').split('/')[1]
	print ((Fore.BLUE + '[*]' + Fore.RESET + ' Testing if are the real IP...'))
	data = "GET /{0} HTTP/1.1\r\nHost: {1}\r\n\r\n".format(home, hncat)

	client = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
	client.connect(( ip, port ))
	client.sendall(data)
	response = client.recv(2048)
	if '200 OK' in response:
		print ((Fore.GREEN + "[+]" + Fore.RESET) + " The Real IP is: %s." % ip)
		sys.exit(1)
	if '301' in response:
		print ((Fore.GREEN + "[+]" + Fore.RESET) + " The Real IP is: %s." % ip)
		sys.exit(1)
	else:
		print ((Fore.RED + "[-]" + Fore.RESET) + " %s is not the IP." %ip)
		print ((Fore.BLUE + '[*]' + Fore.RESET) + ' Trying to DIG for obtain the Real IP')
netcat(domain)

try:
	dream_dns = [item.address for server in dns for item in sys_r.query(server)]
	dream_r = Resolver()
	dream_r.nameservers = dream_dns	
	answer = dream_r.query(domain, 'A')
	for A in answer.rrset.items:
		print (Fore.GREEN + '[+]' + Fore.RESET) + ' Possible IP:', A
except:
	print (Fore.RED + '[-]' + Fore.RESET) + ' IP not found.'
	print ("\n - Exiting...")
	sys.exit(1)
	
def Checking_IP(domain):
	#print(Fore.YELLOW + logo)
	url = 'http://' + domain
	print((Fore.BLUE + '[*]') + Fore.RESET + ' Retrieving target homepage at: %s' % url)
	try:
		org_response = requests.get(url, timeout=config['http_timeout_seconds'])
	except requests.exceptions.Timeout:
		sys.stderr.write((Fore.RED + "[-]" + Fore.RESET) + " %s timed out after %d seconds.\n" % (url, config['http_timeout_seconds']))
		exit(1)
	except requests.exceptions.RequestException as e:
		sys.stderr.write((Fore.RED + "[-]" + Fore.RESET) + " Failed to retrieve %s.\n" % url)
		exit(1)

	if org_response.status_code != 200:
		print (Fore.RED + '[-]' + Fore.RESET) + ' %s responded with an unexpected HTTP status code %d' % (url, org_response.status_code)
		exit(1)

	if org_response.url != url:
		print ((Fore.BLUE + '[*]' + Fore.RESET) + ' %s redirects to %s.' % (url, org_response.url))
		print ('\n - Redirecting to %s.' % org_response.url)
		print ('\n' + Fore.GREEN + "[+]" + Fore.RESET + " Request redirected successful to %s." % org_response.url)
	print ((Fore.BLUE + '[*]' + Fore.RESET + ' Testing if body content is the same in both websites.'))
	
	sec_response = requests.get('http://' + str(A), timeout=config['http_timeout_seconds'])
	if sec_response.status_code != 200:
		print (Fore.RED + '[-]' + Fore.RESET) + ' %s responded with an unexpected HTTP status code %d' % (url, org_response.status_code)
		exit(1)
	if sec_response.text == org_response.text:
		print ((str(A), 'HTML content identical to %s' % domain))
	page_similarity = similarity(sec_response.text, org_response.text)
	if page_similarity > config['response_similarity_threshold']:
		print (((Fore.GREEN + '[+]' + Fore.RESET) + ' HTML content is %d%% structurally similar to: %s' % (round(100 *page_similarity, 2), org_response.url)))
	else:
		print (Fore.RED + '[-]' + Fore.RESET + ' %s is not the real IP.' % str(A))
	return org_response

def netcat2(domain):
	ip = str(A)
	url = 'http://' + domain
	page = requests.get(url, timeout=config['http_timeout_seconds'])
	hncat = page.url.replace('https://www.', '').split('/')[0]
	home = page.url.replace('https://', '').split('.')[-2]
	home2 = home.replace('com', '').split('/')[1]
	print ((Fore.BLUE + '[*]' + Fore.RESET + ' Testing if are the correct IP...'))
	data = "GET /{0} HTTP/1.1\r\nHost: {1}\r\n\r\n".format(home, hncat)

	client = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
	client.connect(( ip, port ))
	client.sendall(data)
	response = client.recv(2048)
	if '200 OK' in response:
		print ((Fore.GREEN + "[+]" + Fore.RESET) + " The Real IP is: %s." % ip)
		sys.exit(1)
	if '301' in response:
		print ((Fore.GREEN + "[+]" + Fore.RESET) + " The Real IP is: %s." % ip)
		sys.exit(1)
	else:
		print ((Fore.RED + "[-]" + Fore.RESET) + " %s is not the IP." %ip)
		sys.exit(1)

if __name__=="__main__":
	Checking_IP(domain),
	netcat2(domain)