# Cloudmare

Cloudmare is a simple tool to find origin servers of websites protected by CloudFlare with a misconfiguration DNS.

For more detail about this common misconfiguration and how Cloudmare works, send me a private message.

Here's what Cloudmare looks like in action.

```
$ python Cloudmare.py target.site -s sub.myvulnerable.site

  ____ _                 _ __  __                
 / ___| | ___  _   _  __| |  \/  | __ _ _ __ ___ 
| |   | |/ _ \| | | |/ _` | |\/| |/ _` | '__/ _ \                  
| |___| | (_) | |_| | (_| | |  | | (_| | | |  __/
 \____|_|\___/ \__,_|\__,_|_|  |_|\__,_|_|  \___|
  
 ================================================
 ||                  Secmare                   ||
 ||            twitter.com/secmare             ||
 ||                   v1.0                     ||
 ================================================

Cloudflare IP Catcher (Auto DIG)...
[*] Checking if sub.myvulnerable.site are similar to target.site...
[-] Sorry, but HTML content is 0% structurally similar to target.site

 - Trying to check with IP... 

[*] Testing if are the real IP...
[-] 123.56.45.49 is not the IP.
[*] Trying to DIG for obtain the Real IP
[+] Possible IP: 23.56.48.62
[*] Retrieving target homepage at: http://target.site
[*] http://target.site redirects to https://www.target.site/home.php.

 - Redirecting to https://www.target.site/home.php.

[+] Request redirected successful to https://www.target.site/home.php.
[*] Testing if body content is the same in both websites.
[+] HTML content is 100% structurally similar to: https://www.target.site/home.php
[*] Testing if are the correct IP...
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
$ python cloudmare.py target.site -s sub.myvulnerable.site
```

## Usage

```
$ python cloudmare.py --help

usage: Cloudmare.py [-h] [-s SUBDOMAIN] [-v] [domain]

positional arguments:
  [domain]       The domain to scan.

optional arguments:
  -h, --help     show this help message and exit
  -s SUBDOMAIN   Server to compare with target. (default: None)
  -v, --version  show program's version number and exit
```

## Compatibility

Tested on Python 2.7 in Kali Linux. Feel free to [open an issue](https://github.com/MrH0wl/Cloudmare/issues/new) if you have bug reports or questions.
