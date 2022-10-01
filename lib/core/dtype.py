#!/usr/bin/env python

import copy
import types

# taken from: 'https://github.com/sqlmapproject/sqlmap'


class AttribDict(dict):
    def __init__(self, _dict=None, attrib=None):
        if _dict is None:
            _dict = {}

        self.attrib = attrib
        dict.__init__(self, _dict)

    def __getattr__(self, item):
        try:
            return self.__getitem__(item)
        except KeyError:
            raise AttributeError("Error accessing to '%s'" % item)

    def __setattr__(self, item, value):
        if "_AttribDict__initialised" not in self.__dict__:
            return dict.__setattr__(self, item, value)

        elif item in self.__dict__:
            dict.__setattr__(self, item, value)

        else:
            self.__setitem__(item, value)

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, dict):
        self.__dict__ = dict

    def __deepcopy__(self, memo):
        retVal = self.__class__()
        memo[id(self)] = retVal

        for attr in dir(self):
            if not attr.startswith('_'):
                value = getattr(self, attr)
                if not isinstance(value, (types.BuiltinFunctionType, types.FunctionType, types.MethodType)):
                    setattr(retVal, attr, copy.deepcopy(value, memo))

        for key, value in self.items():
            retVal.__setitem__(key, copy.deepcopy(value, memo))

        return retVal
