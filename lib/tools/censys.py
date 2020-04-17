import os, sys
import thirdparty.censys.ipv4

from lib.parse.colors import white, green, red, yellow, end, info, que, bad, good, run

def censys(domain):
	censys_ip = []
	creds = None if os.path.getsize('./data/censys_api.txt') is 0 else open('./data/censys_api.txt','r').read()
	creds = creds.split(":") if creds is not None else None
	if creds != None:
		ID = creds[0]
		SECRET = creds[1]
	
	elif sys.version_info[0] == 3:
		ID = input("\n" +info + 'Please enter your censys ID: ')
		SECRET = input(info + 'Now, please enter your censys SECRET: ')

	else:
		ID = raw_input(info + 'Please enter your censys ID: ')
		SECRET = raw_input(info + 'Now, please enter your censys SECRET: ')
	try:
		if creds == None:
			question = input(que + 'Do you want to save your censys.io credentials? y/n: ') if sys.version_info[0] == 3 else raw_input(que + 'Do you want to save your censys.io credentials? y/n: ')
			if question in ["yes", "y", "Y", "ye"]:
				with open("./data/censys_api.txt","w") as f:
					f.write("{0}:{1}".format(ID, SECRET))	
	except:
		pass
	try:
		ip = ['ip']
		c = thirdparty.censys.ipv4.CensysIPv4(api_id=ID, api_secret=SECRET)
		query = list(c.search('{0}'.format((domain)), ip, max_records=10))
		ip_data = [query[i]['ip'] for i in range(len(query))]
		if ip_data:
			for ips in ip_data:
				censys_ip.append(ips)
		return censys_ip
	except Exception as e:
		print(bad + "[ERROR]: " + str(e))