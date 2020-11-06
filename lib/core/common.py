import os
import random
import logging
import warnings

from thirdparty.odict.odict import OrderedDict
from lib.parse.colors import W, B, Y, R, good, bad, run, tab, info, que

def checkFile(filename, raiseOnError=True):
    valid = True

    if filename:
        filename = filename.strip('"\'')
    else:
        try:
            if filename is None or not os.path.isfile(filename):
                valid = False
        except:
            valid = False

        if valid:
            try:
                with open(filename, "rb"):
                    pass
            except:
                valid = False

    if not valid and raiseOnError:
        raise warnings("unable to read file '%s'" % filename)

    return valid

def getFile(filename, commentPrefix='#', lowercase=False, unique=False):

    retVal = list() if not unique else OrderedDict()

    if filename:
        filename = filename.strip('"\'')

    checkFile(filename)

    try:
        with open(filename, 'r') as f:
            for l in f:
                if commentPrefix:
                    if l.find(commentPrefix) != -1:
                        l = l[:l.find(commentPrefix)]

                line = line.strip()

                if line:
                    if lowercase:
                        line = line.lower()

                    if unique and line in retVal:
                        continue

                    if unique:
                        retVal[line] = True
                    else:
                        retVal.append(line)
    except (IOError, OSError, MemoryError) as ex:
        errMsg = "something went wrong while trying "
        errMsg += "to read the content of file '%s' ('%s')" % (filename, (ex))
        raise warnings(errMsg)

    return retVal if not unique else list(retVal.keys())

def setRandomAgent():
    userAgents = open('data/txt/random_agents.txt', 'r')
    if not userAgents:
        debugMsg = info + "loading random HTTP User-Agent header(s) from "
        debugMsg += "file 'data/txt/random_agents.txt'"
        logging.debug(debugMsg)

        try:
            userAgents = getFile('data/txt/random_agents.txt')
        except IOError:
            errMsg = "unable to read HTTP User-Agent file "
            errMsg += "file 'data/txt/random_agents.txt'"
            raise warnings(errMsg)

    return random.sample(userAgents, 1)[0]