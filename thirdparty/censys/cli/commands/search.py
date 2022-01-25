"""Censys search CLI."""
import argparse
import sys
import webbrowser
from typing import List
from urllib.parse import urlencode

from censys.cli.utils import INDEXES, V1_INDEXES, V2_INDEXES, err_console, write_file
from censys.common.exceptions import CensysCLIException
from censys.search import SearchClient

Results = List[dict]

DEFAULT_FIELDS = {
    "certs": [
        "metadata.updated_at",
        "parsed.issuer.common_name",
        "parsed.names",
        "parsed.serial_number",
        "parsed.self_signed",
        "parsed.subject.common_name",
        "parsed.validity.start",
        "parsed.validity.end",
        "parsed.validity.length",
        "metadata.source",
        "metadata.seen_in_scan",
        "tags",
    ],
}


def cli_search(args: argparse.Namespace):
    """Search subcommand.

    Args:
        args (Namespace): Argparse Namespace.

    Raises:
        CensysCLIException: If invalid options are provided.
    """
    index_type = args.index_type or args.query_type

    if args.open:
        url_query = {"q": args.query}
        if index_type in {"certs", "certificates"}:
            webbrowser.open(
                f"https://search.censys.io/certificates?{urlencode(url_query)}"
            )
            sys.exit(0)
        if index_type in V2_INDEXES:
            url_query.update({"resource": index_type})
            webbrowser.open(f"https://search.censys.io/search?{urlencode(url_query)}")
            sys.exit(0)

    censys_args = {}

    if args.api_id:
        censys_args["api_id"] = args.api_id

    if args.api_secret:
        censys_args["api_secret"] = args.api_secret

    c = SearchClient(**censys_args)

    search_args = {}
    write_args = {"file_format": args.format, "file_path": args.output}

    if index_type in V1_INDEXES:
        index = getattr(c.v1, index_type)

        if args.max_records:
            search_args["max_records"] = args.max_records

        fields: List[str] = []
        if args.fields:
            if args.overwrite:
                fields = args.fields
            else:
                fields = args.fields + DEFAULT_FIELDS[index_type]
                # Remove duplicates
                fields = list(set(fields))
            write_args["csv_fields"] = fields

        if len(fields) > 20:
            raise CensysCLIException(
                "Too many fields specified. The maximum number of fields is 20."
            )

        search_args["fields"] = fields

        with err_console.status("Searching"):
            results = list(index.search(args.query, **search_args))
    elif index_type in V2_INDEXES:
        if args.format == "csv":
            raise CensysCLIException(
                "The CSV file format is not valid for Search 2.0 responses."
            )
        index = getattr(c.v2, index_type)

        if args.pages:
            search_args["pages"] = args.pages

        if args.virtual_hosts:
            search_args["virtual_hosts"] = args.virtual_hosts

        with err_console.status("Searching"):
            query = index.search(args.query, **search_args)

            results = []
            for hits in query:
                results += hits

    try:
        write_file(results, **write_args)
    except ValueError as error:  # pragma: no cover
        err_console.print(f"Error writing log file. Error: {error}")


def include(parent_parser: argparse._SubParsersAction, parents: dict):
    """Include this subcommand into the parent parser.

    Args:
        parent_parser (argparse._SubParsersAction): Parent parser.
        parents (dict): Parent arg parsers.
    """
    search_parser = parent_parser.add_parser(
        "search",
        description="Query Censys Search for resource data by providing a query \
            string, the resource index, and the fields to be returned",
        help="query Censys search",
        parents=[parents["auth"]],
    )
    search_parser.add_argument(
        "query",
        type=str,
        help="a string written in Censys Search syntax",
    )

    index_metavar = "|".join(INDEXES)
    index_default = "hosts"
    search_parser.add_argument(
        "--index-type",
        type=str,
        default=index_default,
        choices=INDEXES,
        metavar=index_metavar,
        help="which resource index to query",
    )
    # Backwards compatibility
    search_parser.add_argument(
        "--query_type",
        type=str,
        default=index_default,
        choices=INDEXES,
        metavar=index_metavar,
        help=argparse.SUPPRESS,
    )
    search_parser.add_argument(
        "-f",
        "--format",
        type=str,
        default="screen",
        choices=["screen", "json", "csv"],
        metavar="screen|json|csv",
        help="format of output",
    )
    search_parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="output file path",
    )
    search_parser.add_argument(
        "-O",
        "--open",
        action="store_true",
        help="open query in browser",
    )

    v2_group = search_parser.add_argument_group(
        f"v2 specific arguments ({', '.join(V2_INDEXES)})"
    )
    v2_group.add_argument(
        "--pages",
        default=1,
        type=int,
        help="number of pages of results to return (when set to -1 returns all pages available)",
    )
    v2_group.add_argument(
        "--virtual-hosts",
        type=str,
        default="EXCLUDE",
        choices=["INCLUDE", "EXCLUDE", "ONLY"],
        metavar="INCLUDE|EXCLUDE|ONLY",
        help="whether to include virtual hosts in the results",
    )

    v1_group = search_parser.add_argument_group(
        f"v1 specific arguments ({', '.join(V1_INDEXES)})"
    )
    v1_group.add_argument("--fields", nargs="+", help="list of index-specific fields")
    v1_group.add_argument(
        "--overwrite",
        action="store_true",
        default=False,
        help="overwrite instead of append fields returned by default \
            with fields provided in the fields argument",
    )
    v1_group.add_argument(
        "--max-records",
        type=int,
        help="maximum number of results to return",
    )

    search_parser.set_defaults(func=cli_search)
