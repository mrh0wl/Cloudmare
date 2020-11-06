# Copyright (C) Dnspython Contributors, see LICENSE for text of ISC license

# Copyright (C) 2006-2017 Nominum, Inc.
#
# Permission to use, copy, modify, and distribute this software and its
# documentation for any purpose with or without fee is hereby granted,
# provided that the above copyright notice and this permission notice
# appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND NOMINUM DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL NOMINUM BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
# OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

"""DNS Reverse Map Names."""

import binascii

import thirdparty.dns.name
import thirdparty.dns.ipv6
import thirdparty.dns.ipv4

ipv4_reverse_domain = thirdparty.dns.name.from_text('in-addr.arpa.')
ipv6_reverse_domain = thirdparty.dns.name.from_text('ip6.arpa.')


def from_address(text, v4_origin=ipv4_reverse_domain,
                 v6_origin=ipv6_reverse_domain):
    """Convert an IPv4 or IPv6 address in textual form into a Name object whose
    value is the reverse-map domain name of the address.

    *text*, a ``str``, is an IPv4 or IPv6 address in textual form
    (e.g. '127.0.0.1', '::1')

    *v4_origin*, a ``thirdparty.dns.name.Name`` to append to the labels corresponding to
    the address if the address is an IPv4 address, instead of the default
    (in-addr.arpa.)

    *v6_origin*, a ``thirdparty.dns.name.Name`` to append to the labels corresponding to
    the address if the address is an IPv6 address, instead of the default
    (ip6.arpa.)

    Raises ``thirdparty.dns.exception.SyntaxError`` if the address is badly formed.

    Returns a ``thirdparty.dns.name.Name``.
    """

    try:
        v6 = thirdparty.dns.ipv6.inet_aton(text)
        if thirdparty.dns.ipv6.is_mapped(v6):
            parts = ['%d' % byte for byte in v6[12:]]
            origin = v4_origin
        else:
            parts = [x for x in str(binascii.hexlify(v6).decode())]
            origin = v6_origin
    except Exception:
        parts = ['%d' %
                 byte for byte in thirdparty.dns.ipv4.inet_aton(text)]
        origin = v4_origin
    return thirdparty.dns.name.from_text('.'.join(reversed(parts)), origin=origin)


def to_address(name, v4_origin=ipv4_reverse_domain,
               v6_origin=ipv6_reverse_domain):
    """Convert a reverse map domain name into textual address form.

    *name*, a ``thirdparty.dns.name.Name``, an IPv4 or IPv6 address in reverse-map name
    form.

    *v4_origin*, a ``thirdparty.dns.name.Name`` representing the top-level domain for
    IPv4 addresses, instead of the default (in-addr.arpa.)

    *v6_origin*, a ``thirdparty.dns.name.Name`` representing the top-level domain for
    IPv4 addresses, instead of the default (ip6.arpa.)

    Raises ``thirdparty.dns.exception.SyntaxError`` if the name does not have a
    reverse-map form.

    Returns a ``str``.
    """

    if name.is_subdomain(v4_origin):
        name = name.relativize(v4_origin)
        text = b'.'.join(reversed(name.labels))
        # run through inet_ntoa() to check syntax and make pretty.
        return thirdparty.dns.ipv4.inet_ntoa(thirdparty.dns.ipv4.inet_aton(text))
    elif name.is_subdomain(v6_origin):
        name = name.relativize(v6_origin)
        labels = list(reversed(name.labels))
        parts = []
        for i in range(0, len(labels), 4):
            parts.append(b''.join(labels[i:i + 4]))
        text = b':'.join(parts)
        # run through inet_ntoa() to check syntax and make pretty.
        return thirdparty.dns.ipv6.inet_ntoa(thirdparty.dns.ipv6.inet_aton(text))
    else:
        raise thirdparty.dns.exception.SyntaxError('unknown reverse-map address family')
