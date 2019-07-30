import thirdparty.dnsdumpster
from thirdparty.dnsdumpster.DNSDumpsterAPI import DNSDumpsterAPI
from lib.parse.colors import white, green, red, yellow, end, info, que, bad, good, run

def subdomain_tracking(domain):
	print (yellow + "Tracking subdomains and MX records...\n" + end)
	ip_takes = []
	res = DNSDumpsterAPI(False).search(domain)
	if res['dns_records']['host']:
		print (que + "Subdomains:" + end)
		for entry in res['dns_records']['host']:
			print ("   " + good + "{ip}".format(**entry) + white +  " from: " + "{domain}".format(**entry) + end)
	if res['dns_records']['mx']:
		print (que + "MX Records:" + end)
		for entry in res['dns_records']['mx']:
			print ("   " + good + "{ip}".format(**entry) + white + " from: " + "{domain}".format(**entry) + end)
	print(que + "Enumerating misconfigured DNS subdomains:")

	try:
		for entry in res['dns_records']['host']:
			provider = str(entry['provider'])
			ip = str(entry['ip'])
			if "Cloudflare" not in provider and ip not in ip_takes:
				ip_takes.append('{ip}'.format(**entry))
				print ("   " + good + "{ip}".format(**entry) + " from: " + "{domain}".format(**entry) + end)
		for entry in res['dns_records']['mx']:
			provider = str(entry['provider'])
			ip = str(entry['ip'])
			if "Cloudflare" not in provider and ip not in ip_takes:
				ip_takes.append('{ip}'.format(**entry))
				print ("   " + good + "{ip}".format(**entry) + " from: " + "{domain}".format(**entry) + end)

	except:
		print("   " + bad + " Subdomains and MX records belong Cloudflare Network" + end)
		exit(1)
	if ip_takes != None:
		with open('subdomain.txt', 'w+') as file:
			ip_takes = map(str, ip_takes)
			line = "\n".join(ip_takes)
			file.write(line)
			file.close()
