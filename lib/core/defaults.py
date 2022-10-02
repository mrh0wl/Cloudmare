#!/usr/bin/env python

from lib.core.dtype import AttribDict

defaults = {
    "verbose": True,
    "threads": 1,
    "torPort": 9050,
    "torType": "SOCKS5",
}

defaults = AttribDict(defaults)
