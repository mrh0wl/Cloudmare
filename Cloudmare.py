#!/usr/bin/env python
# coding: utf-8
# By: MrH0wl

from __future__ import print_function

try:
	import os
	import sys
	import socket
	import thirdparty.requests as requests
	import thirdparty.urllib3 as urllib3

	from lib.parse.colors import white, green, red, yellow, end, info, que, bad, good, run
	from lib.parse.cmdline import parse_args, parse_error
	from lib.core.settings import osclear, quest, logotype
except KeyboardInterrupt:
	quest(question=info + 'Are you sure you want to exit? y/n: ', doY="osclear(logotype = logotype(), unknown = bad + 'Sorry, but cannot clear this OS')", doN="continue")


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
config = {
	'http_timeout_seconds': 3,
	'response_similarity_threshold': 0.9
}

try:
	import lxml
except ImportError:
	logotype()
	quest(question=(info + 'WARNING: A module is required. Do you want to install? y/n: '), doY = "pipmain(['install', 'lxml'])", doN = "sys.exit()")

from thirdparty.html_similarity import similarity
from lib.core.dnslookup import Checking_DNS, Resolver
from lib.core.subdomain_finder import subdomain_tracking

def put_file():
	line = open('subdomain.txt', 'r+')
	file = line.readline().replace("\n", "")
	line.close
	return file

def first_scan():
	try:
		print("\n" + yellow +"Tracking IP (Auto DIG)...\n")
		print(que + "Checking if {0} is similar to {1}".format(ns, domain))
		test1 = requests.get('http://' + domain, timeout=config['http_timeout_seconds'])
		test2 = requests.get('http://' + ns, timeout=config['http_timeout_seconds'])
		page_similarity2 = similarity(test1.text, test2.text)
		if page_similarity2 > config['response_similarity_threshold']:
			print ('   ' + good) + 'HTML content is %d%% structurally similar to: %s' % (round(100 *page_similarity2, 2), domain)
		else:
			print ('   ' + bad + 'Sorry, but HTML content is %d%% structurally similar to %s' % (round(100 *page_similarity2, 2), domain))
	except requests.exceptions.Timeout:
		sys.stderr.write("   " + bad + "Connection cannot be established. Try another method\n")
		exit(1)

def first_nc(domain):
	ip = socket.gethostbyname(ns)
	url = 'http://' + domain
	page = requests.get(url, timeout=config['http_timeout_seconds'])
	hncat = page.url.replace('https://www.', '').split('/')[0]
	home = page.url.replace('https://', '').split('.')[-2]
	print (que + 'Testing if it is the real IP')
	data = "GET /{0} HTTP/1.1\r\nHost: {1}\r\n\r\n".format(home, hncat)

	client = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
	client.connect(( ip, 80 ))
	client.sendall(data.encode())
	response = client.recv(4096)
	response = str(response)
	if '200 OK' in response:
		print ("   " + good + "The Real IP is: %s" % ip)
		exit(1)
	elif '301' in response:
		print ("   " + good + "The Real IP is: %s" % ip)
		exit(1)
	else:
		print ("   " + bad + "%s Not the IP." %ip)
		print (que + 'Using DIG to get the real IP')


def Checking_IP(domain):
	A = Checking_DNS(ns, dns)
	print ('   ' + good + 'Possible IP:', A)
	url = 'http://' + domain
	print(que + ' Retrieving target homepage at: %s' % url)
	try:
		org_response = requests.get(url, timeout=config['http_timeout_seconds'])
	except requests.exceptions.Timeout:
		sys.stderr.write("   " + bad + "%s timed out after %d seconds.\n" % (url, config['http_timeout_seconds']))
		exit(1)
	except requests.exceptions.RequestException as e:
		sys.stderr.write("   " + bad + "Failed to retrieve %s.\n" % url)
		exit(1)

	if org_response.status_code != 200:
		print ('   ' + bad + ' %s responded with an unexpected HTTP status code %d' % (url, org_response.status_code))
		exit(1)

	if org_response.url != url:
		print ('   ' + good + '%s redirects to %s.' % (url, org_response.url))
		print ("   " + good + "Request redirected successful to %s." % org_response.url)
	print (que + 'Testing if body content is the same in both websites.')

	sec_response = requests.get('http://' + str(A), timeout=config['http_timeout_seconds'])
	if sec_response.status_code != 200:
		print ('   ' + good + '%s responded with an unexpected HTTP status code %d' % (url, org_response.status_code))
		exit(1)
	if sec_response.text == org_response.text:
		print ((str(A), 'HTML content identical to %s' % domain))
	page_similarity = similarity(sec_response.text, org_response.text)
	if page_similarity > config['response_similarity_threshold']:
		print ('   ' + good + ' HTML content is %d%% structurally similar to: %s' % (round(100 *page_similarity, 2), org_response.url))
	return org_response

def second_nc(domain):
	A = Checking_DNS(ns, dns)
	ip = str(A)
	url = 'http://' + domain
	page = requests.get(url, timeout=config['http_timeout_seconds'])
	hncat = page.url.replace('https://www.', '').split('/')[0]
	home = page.url.replace('https://', '').split('.')[-2]
	print (que + 'Testing if are the real IP')
	data = "GET /{0} HTTP/1.1\r\nHost: {1}\r\n\r\n".format(home, hncat)

	client = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
	client.connect(( ip, 80 ))
	client.sendall(data)
	response = client.recv(2048)
	if '200 OK' and domain in response:
		print ("   " + good + "The real IP is: %s" % ip)
		exit(1)
	if '301' and domain in response:
		print ("   " + info + "The Real IP is: %s" % ip)
		exit(1)
	else:
		print ("   " + bad + "%s is not the IP" %ip)

if __name__=="__main__":
	try:
		args,sys_r = parse_args(),Resolver()
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
			print (bad + "too few arguments")
			exit(0)

		dns = [ns]
		first_scan()
		first_nc(domain)
		Checking_DNS(ns, dns)
		Checking_IP(domain)
		second_nc(domain)
	except KeyboardInterrupt:
		quest(question=info + 'Are you sure you want to exit? y/n: ', doY="osclear(logotype = logotype(), unknown = bad + 'Sorry, but cannot clear this OS')", doN="continue")
		if sys.platform.lower().startswith(('win32')):
			os.system('cls')
		else:
			os.system('clear')
		logotype()
		print(yellow + "~ Thanks for using this script! <3")
		sys.exit(0)
	except requests.exceptions.ConnectionError as e:
		print('   ' + bad + 'ERROR: Connection cannot be established. Try another method.')
	except Exception as e:
		logger.error(e)
		logger.warn('ERROR: Cannot connect to %s. Please try another method' % (domain))
