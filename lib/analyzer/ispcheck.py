from thirdparty.bs4 import BeautifulSoup
from thirdparty import requests

cloudlist = ['Sucuri',
			'Cloudflare',
			'Incapsula']

def ISPCheck(domain):
	try:
		base = 'https://check-host.net/ip-info?host=' + domain
		base_check = requests.get(base).text
		UrlHTML = BeautifulSoup(base_check, "lxml")
		if UrlHTML.findAll('div', {'class':'error'}):
			get_Content = " - cannot retrieve information "
			return get_Content
		get_Content = str([i for i in UrlHTML.findAll('tr', {'class':'zebra'}) if 'Organization' in str(i)][0].get_text(strip=True).split('Organization')[1])
		for cloud in cloudlist:
			if cloud in get_Content:
				get_Content = " - belong " + cloud
				return get_Content
	except:
		return None
