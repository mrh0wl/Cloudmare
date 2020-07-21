# Cloudmare

Cloudmare is a simple tool to find origin servers of websites protected by CloudFlare with a misconfiguration DNS.

For more detail about this common misconfiguration and how Cloudmare works, send me a private message.

Here's what Cloudmare looks like in action.

![Example usage](https://i.imgur.com/XLpvDb5.png "Example usage")

(_The IP addresses in this example have been obfuscated and replaced by randomly generated IPs_)

## Setup

1) Clone the repository

```
$ git clone https://github.com/MrH0wl/Cloudmare.git
```

2) Go to the folder

```
$ cd cloudmare
$ python Cloudmare.py -h
```

3) Run Cloudmare (see [Usage](#usage) below for more detail)

```
$ python cloudmare.py target.site --subdomain
```

## Usage

![Help options](https://i.imgur.com/sOC0ZQF.png "Help options")

## Compatibility

Tested on Python 2.7 and Python 3.7, working on Linux and Windows. Feel free to [open an issue] if you have bug reports or questions. If you want to collaborate, you're welcome.

[open an issue]: https://github.com/MrH0wl/Cloudmare/issues/new

## Donate BTC

If you wish, you can invite me to a cup of coffee, it only costs 1 USD.

```
>1LhDVkgjgmygW2at1brUtVii9NKPYM1xni
```
