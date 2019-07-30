import thirdparty.dns
import thirdparty.dns.resolver
import thirdparty.dns.exception
from lib.parse.colors import white, green, red, yellow, end, info, que, bad, good, run
from thirdparty.dns.resolver import Resolver


def Checking_DNS(ns, dns):
	try:
		dream_dns = [item.address for server in dns for item in sys_r.query(server)]
		dream_r = Resolver()
		dream_r.nameservers = dream_dns
		answer = dream_r.query(domain, 'A')
		for A in answer.rrset.items:
			A
	except:
		print ('   ' + bad + ' IP not found.')
		print ("\n - Exiting...")
		exit(1)
	return A
	