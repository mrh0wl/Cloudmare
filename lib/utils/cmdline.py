#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging
import sys

from ..core.defaults import defaults
from ..utils.colors import W, Y, bad, warn
from ..utils.settings import (BASIC_HELP, COPYRIGHT, NAME, VERSION,
                              CheckImports, logotype)

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

config = ConfigParser()

try:
    import argparse
    from argparse import SUPPRESS, ArgumentError, ArgumentParser

except ImportError as im:
    err = im.name
    CheckImports(err).downloadLib()

finally:
    def get_actions(instance):
        for attr in ("option_list", "_group_actions", "_actions"):
            if hasattr(instance, attr):
                return getattr(instance, attr)

    def get_groups(parser):
        return getattr(parser, "option_groups", None) or getattr(parser, "_action_groups")

    def get_all_options(parser):
        retVal = set()

        for option in get_actions(parser):
            if hasattr(option, "option_strings"):
                retVal.update(option.option_strings)
            else:
                retVal.update(option._long_opts)
                retVal.update(option._short_opts)

        for group in get_groups(parser):
            for option in get_actions(group):
                if hasattr(option, "option_strings"):
                    retVal.update(option.option_strings)
                else:
                    retVal.update(option._long_opts)
                    retVal.update(option._short_opts)

        return retVal


OBS_OPT = {
    "--dns-bruter": "use '--bruter' instead",
}

DEP_OPT = {
    "--subdomain": "functionality being done automatically",
}


def checkOldOptions(args):
    for _ in args:
        _ = _.split('=')[0].strip()
        if _ in OBS_OPT:
            errMsg = bad + "option '%s' is obsolete" % _
            if OBS_OPT[_]:
                errMsg += " (hint: %s)" % OBS_OPT[_]
            raise logging.warn(errMsg)
        elif _ in DEP_OPT:
            warnMsg = "option '%s' is deprecated" % _
            if DEP_OPT[_]:
                warnMsg += " (hint: %s)" % DEP_OPT[_]
            logging.warn(warnMsg)


def parser_cmd(argv=None):
    logotype()
    def formatter(prog): return argparse.HelpFormatter(prog, max_help_position=100)
    parser = ArgumentParser(usage="Example: python " + Y + sys.argv[0] + W + " -u site.com", formatter_class=formatter)
    try:
        parser.add_argument("--hh", "--help-hack", dest="advancedHelp", action="store_true",
                            help="Show advanced help message and exit")

        parser.add_argument("--version", action='version', version=NAME + VERSION + ' | ' + COPYRIGHT,
                            help="Show program's version number and exit")

        parser.add_argument("-v", dest="verbose", action="store_true",
                            help="Verbosity for sublist3r: True/False (default: False)")

        # Target options
        target = parser.add_argument_group(
            "Target", "At least one of these options has to be provided to define the target(s)")

        target.add_argument("-u", "--url", metavar="target", dest="domain",
                            help="Target URL as first argument (e.g. python Cloudmare.py site.com)")

        target.add_argument("--disable-sublister", dest="disableSub", action="store_true",
                            help="Disable subdomain listing for testing")

        target.add_argument("--bruter", dest="brute", action="store_true",
                            help="Bruteforcing target to find associated domains")

        target.add_argument("--subbruter", dest="subbrute", action="store_true",
                            help="Bruteforcing target's subdomains using subbrute module")

        # Request options
        request = parser.add_argument_group(
            "Request", "These options can be used to specify how to connect to the target URL")

        request.add_argument("--user-agent", dest="uagent",
                             help="Set HTTP User-Agent header value")

        request.add_argument("--random-agent", dest="randomAgent", action="store_true",
                             help="Set randomly selected HTTP User-Agent header value")

        request.add_argument("--host", dest="host",
                             help="HTTP Host header value")

        request.add_argument("--headers", dest="headers",
                             help="Set custom headers (e.g. \"Origin: originwebsite.com, ETag: 123\")")

        request.add_argument("--ignore-redirects", dest="ignoreRedirects", action="store_false",
                             help="Ignore Redirection attempts")

        request.add_argument("--threads", dest="threads", default=defaults.threads, type=int,
                             help="Max number of concurrent HTTP(s) requests (default %d)" % defaults.threads)

        # Search options
        search = parser.add_argument_group("Search", "These options can be used to perform advanced searches")

        search.add_argument("-sC", "--search-censys", dest="censys", nargs="?", const="data/APIs/api.conf", type=str,
                            help="Perform search using Censys API")

        search.add_argument("-sSh", "--search-shodan", dest="shodan", nargs="?", const="data/APIs/api.conf", type=str,
                            help="Perform search using Shodan API")

        search.add_argument("-sSt", "--search-st", dest="securitytrails", nargs="?", const="data/APIs/api.conf",
                            type=str, help="Perform search using Securitytrails API")

        # Output options
        output = parser.add_argument_group("Output", "These options can be used to save the subdomains results")

        output.add_argument("-o", "--output", dest="outSub", action="store_true",
                            help="Save the subdomains into: \"data/output/subdomains-[domain].txt\"")

        output.add_argument("--oG", "--output-good", dest="outSubG", action="store_true",
                            help="Save [good response] subdomains into: \"data/output/good-subdomains-[domain].txt\"")

        output.add_argument("--oI", "--output-ip", dest="outSubIP", action="store_true",
                            help="Save subdomains IP into: \"data/output/good-subdomains-[domain].txt\"")

        advancedHelp = True
        argv = sys.argv[1:]
        checkOldOptions(argv)

        for i in range(len(argv)):
            if argv[i] in ("-h", "--help"):
                advancedHelp = False
                for group in get_groups(parser)[:]:
                    found = False
                    for option in get_actions(group):
                        if option.dest not in BASIC_HELP:
                            option.help = SUPPRESS
                        else:
                            found = True
                    if not found:
                        get_groups(parser).remove(group)

        try:
            (args, _) = parser.parse_known_args(argv) if hasattr(
                parser, "parse_known_args") else parser.parse_args(argv)
        except UnicodeEncodeError as ex:
            print("\n %s%s\n" % bad, ex)
            raise SystemExit
        except SystemExit:
            if "-h" in argv and not advancedHelp or "--help" in argv and not advancedHelp:
                print("\n" + warn + "to see full list of options run with '-hh' or '--help-hack'\n")
            raise

        if not args.domain:
            errMsg = "missing a mandatory option (-u, --url). Use -h for basic and -hh for advanced help\n"
            parser.error(errMsg)

        return parser.parse_args(), parser.error
    except (ArgumentError, TypeError) as ex:
        parser.error(str(ex))
    debugMsg = "parsing command line"
    logging.debug(debugMsg)
