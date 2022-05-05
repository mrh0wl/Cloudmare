# Cloudmare

Cloudmare is a simple tool to find origin servers of websites protected by Cloudflare, Sucuri or Incapsula with a misconfiguration DNS.

For more detail about this common misconfiguration and how Cloudmare works, send me a private message.

Here's what Cloudmare looks like in action.

![Example usage](https://i.imgur.com/pSzOXFG.png "Example usage")

(_The IP addresses in this example have been obfuscated and replaced by randomly generated IPs_)

## Setup

1) Clone the repository

```
$ git clone https://github.com/MrH0wl/Cloudmare.git
```

2) Go to the folder

```
$ cd Cloudmare
$ python Cloudmare.py -h or python Cloudmare.py -hh
```

3) Run Cloudmare (see [Usage](#usage) below for more detail)

```
$ python Cloudmare.py -u target.site --bruter -sC -sSh -sSh --host verified.site
```

## Usage

![Help options](https://i.imgur.com/9pmF1ol.png "Help options")

## Compatibility

Tested on Python 2.7 and Python=<3.7, working on Linux and Windows. Feel free to [open an issue] if you have bug reports or questions. If you want to collaborate, you're welcome.

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

[paypal](https://paypal.me/jackablandon)

## Contact Info
```
✉️Email: secmare@protonmail.com
🐦Twitter: @mrh0wl
📷Instagram: @mrh0wl
```
