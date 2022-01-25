"""Interact with argparser."""
import argparse
import os

from . import commands
from censys.common.config import DEFAULT, get_config


def get_parser() -> argparse.ArgumentParser:
    """Gets ArgumentParser for CLI.

    Returns:
        argparse.ArgumentParser
    """
    config = get_config()

    auth = argparse.ArgumentParser(add_help=False)
    auth.add_argument(
        "--api-id",
        default=os.getenv("CENSYS_API_ID") or config.get(DEFAULT, "api_id"),
        required=False,
        help="a Censys API ID \
            (alternatively you can use the env variable CENSYS_API_ID)",
    )
    auth.add_argument(
        "--api-secret",
        default=os.getenv("CENSYS_API_SECRET") or config.get(DEFAULT, "api_secret"),
        required=False,
        help="a Censys API SECRET \
            (alternatively you can use the env variable CENSYS_API_SECRET)",
    )
    asm_auth = argparse.ArgumentParser(add_help=False)
    asm_auth.add_argument(
        "--api-key",
        default=os.getenv("CENSYS_ASM_API_KEY") or config.get(DEFAULT, "asm_api_key"),
        required=False,
        help="a Censys ASM API Key \
            (alternatively you can use the env variable CENSYS_ASM_API_KEY)",
    )

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        default=False,
        help="display version",
    )

    def print_help(_: argparse.Namespace):
        """Prints help."""
        parser.print_help()
        parser.exit()

    parser.set_defaults(func=print_help)

    subparsers = parser.add_subparsers()

    parents = {
        "auth": auth,
        "asm_auth": asm_auth,
    }
    for command in commands.__dict__.values():
        try:
            include_func = getattr(command, "include")
        except AttributeError:
            continue

        include_func(subparsers, parents)

    return parser
