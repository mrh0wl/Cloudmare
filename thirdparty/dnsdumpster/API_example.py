#!env python
# -*- coding: utf-8 -*-

from dnsdumpster.DNSDumpsterAPI import DNSDumpsterAPI
import base64
domain = 'uber.com'

print('Testing... : {}'.format(domain))

res = DNSDumpsterAPI(True).search(domain)

print("####### Domain #######")
print(res['domain'])

print("\n\n\n####### DNS Servers #######")
for entry in res['dns_records']['dns']:
    print(("{domain} ({ip}) {as} {provider} {country}".format(**entry)))

print("\n\n\n####### MX Records #######")
for entry in res['dns_records']['mx']:
    print(("{domain} ({ip}) {as} {provider} {country}".format(**entry)))

print("\n\n\n####### Host Records (A) #######")
for entry in res['dns_records']['host']:
    if entry['reverse_dns']:
        print(("{domain} ({reverse_dns}) ({ip}) {as} {provider} {country}".format(**entry)))
    else:
        print(("{domain} ({ip}) {as} {provider} {country}".format(**entry)))

print("\n\n\n####### TXT Records #######")
for entry in res['dns_records']['txt']:
	print(entry)

image_retrieved = res['image_data'] is not None
print("\n\n\nRetrieved Network mapping image? {} (accessible in 'image_data')".format(image_retrieved))
print(repr(base64.b64decode(res['image_data'])[:20]) + '...') # to save it somewhere else.

xls_retrieved = res['xls_data'] is not None
print("\n\n\nRetrieved XLS hosts? {} (accessible in 'xls_data')".format(xls_retrieved))
print(repr(base64.b64decode(res['xls_data'])[:20]) + '...') # to save it somewhere else.
# open('tsebo.com.xlsx','wb').write(res['xls_data'].decode('base64')) # example of saving xlsx
