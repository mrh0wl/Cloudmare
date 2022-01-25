"""Censys config CLI."""
import argparse
import sys

from rich import box
from rich.table import Table

from censys.cli.utils import console
from censys.common.exceptions import CensysUnauthorizedException
from censys.search.v2.api import CensysSearchAPIv2


def cli_account(args: argparse.Namespace):  # pragma: no cover
    """Account subcommand.

    Args:
        args: Argparse Namespace.
    """
    try:
        client = CensysSearchAPIv2(args.api_id, args.api_secret)
        account = client.account()
        if args.json:
            console.print_json(data=account)
        else:
            table = Table(
                "Key", "Value", show_header=False, box=box.SQUARE, highlight=True
            )
            table.add_row("Email", account["email"])
            table.add_row("Login ID", account["login"])
            table.add_row("First Login", account["first_login"])
            table.add_row("Last Login", account["last_login"][:-7])
            quota = account["quota"]
            table.add_row(
                "Query Quota",
                f"{quota['used']} / {quota['allowance']} ({quota['used']/quota['allowance'] * 100 :.2f}%)",
            )
            table.add_row("Quota Resets At", quota["resets_at"])
            console.print(table)
        sys.exit(0)
    except CensysUnauthorizedException:
        console.print("Failed to authenticate")
        sys.exit(1)


def include(parent_parser: argparse._SubParsersAction, parents: dict):
    """Include this subcommand into the parent parser.

    Args:
        parent_parser (argparse._SubParsersAction): Parent parser.
        parents (dict): Parent arg parsers.
    """
    account_parser = parent_parser.add_parser(
        "account",
        description="Check Censys account details and quota",
        help="check Censys account details and quota",
        parents=[parents["auth"]],
    )
    account_parser.add_argument(
        "-j", "--json", action="store_true", help="Output in JSON format"
    )
    account_parser.set_defaults(func=cli_account)
