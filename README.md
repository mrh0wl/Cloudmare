# Cloudmare

Cloudmare is a simple tool to find the origin servers of websites protected by Cloudflare, Sucuri, or Incapsula with a misconfigured DNS.

For more details about this common misconfigured and how Cloudmare works, send me a private message.

Here's what Cloudmare looks like in action.

![Example usage](https://i.imgur.com/pSzOXFG.png "Example usage")

(_The websites and the IP addresses in this example have been obfuscated_)

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
3) git clone [https://github.com/MrH0wl/Cloudmare.git](https://github.com/MrH0wl/Cloudmare.git)
4) cd Cloudmare
5) python Cloudmare.py -h or python Cloudmare.py -hh

```
Note: Be patient if the script requires to install modules.
```

## Usage

![Help options](https://i.imgur.com/9pmF1ol.png "Help options")

## Compatibility

Tested on Python>=3.7 (don't use Python 2 anymore), working on Linux and Windows. Feel free to [open an issue] if you have bug reports or questions. If you want to collaborate, you're welcome.

## Donate

If you want Cloudmare to be updated more frequently with many more features, you can donate to help make this happen.

<a href="https://paypal.me/mrh0wl">
<img src="https://i.imgur.com/BtQVHbH.png" alt="Donate with PayPal" width="250"/>
</a>
<a href="https://buymeacoffee.com/mrh0wl">
<img src="https://miro.medium.com/max/720/1*VJdus0nKuy1uNoByh5BN3w.png" alt="Buy me a coffee" width="260"/>
</a>

## Contact Info

```
✉️Email: secmare@protonmail.com
🐦Twitter: @mrh0wl
📷Instagram: @mrh0wl
```

[open an issue]: https://github.com/MrH0wl/Cloudmare/issues/new
