# Cloudmare

Cloudmare is a simple tool to find origin servers of websites protected by CloudFlare with a misconfiguration DNS.

For more detail about this common misconfiguration and how Cloudmare works, send me a private message.

Here's what Cloudmare looks like in action.

```
$ python Cloudmare.py target.site -s
  ____ _                 _ __  __                
 / ___| | ___  _   _  __| |  \/  | __ _ _ __ ___ 
| |   | |/ _ \| | | |/ _` | |\/| |/ _` | '__/ _ \                  
| |___| | (_) | |_| | (_| | |  | | (_| | | |  __/
 \____|_|\___/ \__,_|\__,_|_|  |_|\__,_|_|  \___|
	
 ================================================
 ||                  Secmare                   ||
 ||            twitter.com/secmare             ||
 ||                  v1.4.56                   ||
 ================================================
	
Tracking subdomains and MX records...

[*] Subdomains:
   [+] 104.28.22.23 from: target.site
   [+] 104.28.22.23 from: ns1.target.site
   [+] 123.56.45.42 from: mail2.target.site
   [+] 104.28.22.23 from: ns2.target.site
   [+] 104.28.22.23 from: www.database.target.site
   [+] 104.28.22.23 from: www.forum.target.site
   [+] 104.28.22.23 from: www.target.site
   [+] 123.56.45.49 from: mail.target.site
   [+] 123.56.45.49 from: vps.target.site
[*] MX Records:
   [+] 123.56.45.42 from: 2 mail2.target.site.
   [+] 123.56.45.49 from: 0 mail.target.site.
   [+] 123.56.45.49 from: 10 vps.target.site.

[*]Enumerating misconfigured DNS subdomains:
   [+] 123.56.45.42 from: 2 mail2.target.site.
   [+] 123.56.45.49 from: 0 mail.target.site.
Cloudflare IP Catcher (Auto DIG)...

[*] Checking if 123.56.45.49 are similar to target.site
   [-] Sorry, but HTML content is 0% structurally similar to target.site

 - Trying to check with IP... 

[*] Testing if are the real IP
   [-] 123.56.45.49 is not the IP.
[*] Trying to DIG for obtain the Real IP
   [+] Possible IP: 23.56.48.62
[*] Retrieving target homepage at: http://target.site
[*] http://target.site redirects to https://www.target.site/home.php.

   [+] Request redirected successful to https://www.target.site/home.php.
[*] Testing if body content is the same in both websites.
   [+] HTML content is 100% structurally similar to: https://www.target.site/home.php
[*] Testing if are the real IP
   [+] The Real IP is: 23.56.48.62.

```

(_The IP addresses in this example have been obfuscated and replaced by randomly generated IPs_)

## Setup

1) Clone the repository

```
$ git clone https://github.com/MrH0wl/Cloudmare.git
```

2) Install the dependencies

```
$ cd cloudmare
$ pip install -r requirements.txt
```

3) Run Cloudmare (see [Usage](#usage) below for more detail)

```
$ python cloudmare.py target.site -s
```

## Usage

```
$ python cloudmare.py --help
  ____ _                 _ __  __                
 / ___| | ___  _   _  __| |  \/  | __ _ _ __ ___ 
| |   | |/ _ \| | | |/ _` | |\/| |/ _` | '__/ _ \                  
| |___| | (_) | |_| | (_| | |  | | (_| | | |  __/
 \____|_|\___/ \__,_|\__,_|_|  |_|\__,_|_|  \___|
	
 ================================================
 ||                  Secmare                   ||
 ||            twitter.com/secmare             ||
 ||                   v1.4                     ||
 ================================================
	
usage: Cloudmare.py [-h] [-v] -s [domain]

positional arguments:
  [domain]         The domain to scan

OPTIONS:
  -h, --help       show this help message and exit
  -v, --version    show program's version number and exit
  -s, --subdomain  Scan for subdomain
  -ns, --nameserver Scan using your obtained NameServer


Example: python Cloudmare.py [DOMAIN] -s
```

## Compatibility

Tested on Python 2.7 in Kali Linux. Feel free to [open an issue] if you have bug reports or questions. If you want to collaborate, you're welcome.

[open an issue]: https://github.com/MrH0wl/Cloudmare/issues/new
