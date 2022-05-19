# Cloudmare

Cloudmare is a simple tool to find the origin servers of websites protected by Cloudflare, Sucuri or Incapsula with a misconfiguration DNS.

For more detail about this common misconfiguration and how Cloudmare works, send me a private message.

Here's what Cloudmare looks like in action.

![Example usage](https://i.imgur.com/pSzOXFG.png "Example usage")

(_The IP addresses in this example have been obfuscated and replaced by randomly generated IPs_)

## Setup

1) Clone the repository

```
git clone https://github.com/MrH0wl/Cloudmare.git
```

2) Go to the folder

```
cd Cloudmare
python Cloudmare.py -h or python Cloudmare.py -hh
```

3) Run Cloudmare (see [Usage](#usage) below for more detail)

```
python Cloudmare.py -u target.site --bruter -sC -sSh -sSt --host verified.site
```

(Remember to view -hh for more info about the arguments)

## Termux users

1) pkg upgrade && pkg update
2) pkg install git python libxml2 libxslt dnsutils
3) git clone <https://github.com/MrH0wl/Cloudmare.git>
4) cd Cloudmare
5) python Cloudmare.py -h or python Cloudmare.py -hh

```
Note: Be patient if the script requires to install modules.
```

## Usage

![Help options](https://i.imgur.com/9pmF1ol.png "Help options")

## Compatibility

Tested on Python=<3.7 (don't use Python 2 more), working on Linux and Windows. Feel free to [open an issue] if you have bug reports or questions. If you want to collaborate, you're welcome.

[open an issue]: https://github.com/MrH0wl/Cloudmare/issues/new

## Donate BTC

If you want Cloudmare to be updated more frequently with many more features, you can donate to help make this happen.

BTC:

```
15y7CTsrJeLmJuKzWXT8BVRoxEPXbK4Zp5
```

ETH:

```
0x9665C32ba7dD6e7C8278ff788303B937aA9b2f41
```

[![](https://raw.githubusercontent.com/aha999/DonateButtons/master/Paypal.png)](https://paypal.me/mrh0wl)

## Contact Info

```
✉️Email: secmare@protonmail.com
🐦Twitter: @mrh0wl
📷Instagram: @mrh0wl
```
