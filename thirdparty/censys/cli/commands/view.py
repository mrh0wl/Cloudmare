"""Censys view CLI."""
import argparse
import sys
import webbrowser

from censys.cli.utils import V2_INDEXES, console, valid_datetime_type, write_file
from censys.search import SearchClient
from censys.search.v2.api import CensysSearchAPIv2


def cli_view(args: argparse.Namespace):
    """Search subcommand.

    Args:
        args (Namespace): Argparse Namespace.
    """
    if args.open:
        webbrowser.open(
            f"https://search.censys.io/{args.index_type}/{args.document_id}"
        )
        sys.exit(0)

    censys_args = {}

    if args.api_id:
        censys_args["api_id"] = args.api_id

    if args.api_secret:
        censys_args["api_secret"] = args.api_secret

    c = SearchClient(**censys_args)

    index: CensysSearchAPIv2 = getattr(c.v2, args.index_type)

    view_args = {}
    write_args = {
        "file_format": "json" if args.output else "screen",
        "file_path": args.output,
        "base_name": f"censys-view-{args.document_id}",
    }

    if args.at_time:
        view_args["at_time"] = args.at_time

    document = index.view(args.document_id, **view_args)

    try:
        write_file(document, **write_args)
    except ValueError as error:  # pragma: no cover
        console.print(f"Error writing log file. Error: {error}")


def include(parent_parser: argparse._SubParsersAction, parents: dict):
    """Include this subcommand into the parent parser.

    Args:
        parent_parser (argparse._SubParsersAction): Parent parser.
        parents (dict): Parent arg parsers.
    """
    view_parser = parent_parser.add_parser(
        "view",
        description="View a document in Censys Search by providing a document \
            id and the resource index",
        help="view document",
        parents=[parents["auth"]],
    )
    view_parser.add_argument(
        "document_id",
        type=str,
        help="a document id (IP address) to view",
    )
    view_parser.add_argument(
        "--index-type",
        type=str,
        default="hosts",
        choices=V2_INDEXES,
        metavar="|".join(V2_INDEXES),
        help="which resource index to query",
    )
    view_parser.add_argument(
        "--at-time",
        type=valid_datetime_type,
        metavar="YYYY-MM-DD (HH:mm)",
        help="Fetches a document at a given point in time",
    )
    view_parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="json output file path",
    )
    view_parser.add_argument(
        "-O",
        "--open",
        action="store_true",
        help="open document in browser",
    )
    view_parser.set_defaults(func=cli_view)
