#!/usr/bin/env python
"""
Interact with the Censys Search API through the command line.
"""

import os
import sys
import csv
import time
import json
import argparse
from pathlib import Path
from typing import Union, Optional, List, Tuple

import thirdparty.requests

from thirdparty.censys.base import CensysAPIBase
from thirdparty.censys.config import get_config, write_config, DEFAULT
from thirdparty.censys.ipv4 import CensysIPv4
from thirdparty.censys.websites import CensysWebsites
from thirdparty.censys.certificates import CensysCertificates
from thirdparty.censys.exceptions import (
    CensysCLIException,
    CensysNotFoundException,
    CensysUnauthorizedException,
)

Fields = List[str]
Results = List[dict]
Index = Union[CensysIPv4, CensysWebsites, CensysCertificates]


class CensysAPISearch:
    """
    This class searches the Censys API, taking in options from the command line and
    returning the results to a CSV or JSON file, or to stdout.

    Args:
        api_id (str, optional): The API ID provided by Censys.
        api_secret (str, optional): The API secret provided by Censys.
        start_page (int, optional): Page number to start from. Defaults to 1.
        max_pages (int, optional): The maximum number of pages. Defaults to 10.
    """

    csv_fields: Fields = list()
    """A list of fields to be used by the CSV writer."""

    def __init__(self, **kwargs):
        self.api_user = kwargs.get("api_id")
        self.api_pass = kwargs.get("api_secret")
        self.start_page = kwargs.get("start_page", 1)
        self.max_pages = kwargs.get("max_pages", 10)

    @staticmethod
    def _write_csv(file_path: str, search_results: Results, fields: Fields) -> bool:
        """
        This method writes the search results to a new file in CSV format.

        Args:
            file_path (str): Name of the file to write to on the disk.
            search_results (Results): A list of results from the query.
            fields (Fields): A list of fields to write as headers.

        Returns:
            bool: True if wrote to file successfully.
        """

        with open(file_path, "w") as output_file:
            if search_results and isinstance(search_results, list):
                # Get the header row from the first result
                writer = csv.DictWriter(output_file, fieldnames=fields)
                writer.writeheader()

                for result in search_results:
                    # Use the Dict writer to process and write results to CSV
                    writer.writerow(result)

        print(f"Wrote results to file {file_path}")

        # method returns True, if the file has been written successfully.
        return True

    @staticmethod
    def _write_json(file_path: str, search_results: Results) -> bool:
        """
        This method writes the search results to a new file in JSON format.

        Args:
            file_path (str): Name of the file to write to on the disk.
            search_results (Results): A list of results from the query.

        Returns:
            bool: True if wrote to file successfully.
        """

        with open(file_path, "w") as output_file:
            # Since the results are already in JSON, just write them to a file.
            json.dump(search_results, output_file, indent=4)

        print(f"Wrote results to file {file_path}")
        return True

    @staticmethod
    def _write_screen(search_results: Results) -> bool:
        """
        This method writes the search results to screen.

        Args:
            search_results (Results): A list of results from the query.

        Returns:
            bool: True if wrote to file successfully.
        """

        print(json.dumps(search_results, indent=4))
        return True

    def write_file(
        self,
        results_list: Results,
        file_format: str = "screen",
        file_path: Optional[str] = None,
    ) -> bool:
        """
        This method just sorts which format will be used to store
        the results of the query.

        Args:
            results_list (Results): A list of results from the API query.
            file_format (str, optional): The format of the output.
            file_path (str optional): A path to write results to.

        Returns:
            bool: True if wrote out successfully.
        """

        if file_format and isinstance(file_format, str):
            file_format = file_format.lower()

        if not file_path:
            # This method just creates some dynamic file names
            file_name_ext = f"{time.time()}.{file_format}"
            file_path = f"censys-query-output.{file_name_ext}"

        if file_format == "json":
            return self._write_json(file_path, results_list)
        if file_format == "csv":
            return self._write_csv(file_path, results_list, fields=self.csv_fields)
        return self._write_screen(results_list)

    def _combine_fields(
        self, default_fields: Fields, user_fields: Fields, overwrite: bool = False,
    ) -> Fields:
        """
        This method is used to specify which fields will be returned in the results.

        Args:
            default_fields (Fields): A list of fields that are returned by default.
            user_fields (Fields): A list of user-specified fields. Max 20.
            overwrite (bool, optional): Whether to overwrite or append default fields
                                        with user fields. Defaults to False.

        Raises:
            CensysCLIException: Too many fields specified.

        Returns:
            Fields: A list of fields.
        """

        field_list: Fields = default_fields

        if user_fields:
            if overwrite:
                field_list = user_fields
            else:
                field_list = list(set(user_fields + default_fields))

        # This is the hard limit for the number of fields that can be in a query.
        if len(list(field_list)) > 20:
            raise CensysCLIException(
                "Too many fields specified. The maximum number of fields is 20."
            )

        self.csv_fields = list(field_list)
        return list(field_list)

    def _process_search(
        self, query: str, search_index: Index, fields: Fields
    ) -> Results:
        """
        This method provides a common way to process searches from the API.

        Args:
            query (str): The string to send to the API as a query.
            search_index (Index): The data set to be queried.
            fields (Fields): A list of fields to be returned for each result.

        Returns:
            Results: A list of results from the query.
        """

        records = []

        while True:
            response = search_index.paged_search(
                query=query, fields=fields, page=self.start_page
            )

            for record in response["results"]:
                records.append(record)

            # Break while loop when last page is reached
            if (
                response["metadata"]["page"] >= response["metadata"]["pages"]
                or response["metadata"]["page"] >= self.max_pages
            ):
                break

            self.start_page += 1

        return records

    def search_ipv4(self, **kwargs) -> Results:
        """
        A method to search the IPv4 data set via the API.

        Args:
            query (str): The string search query.
            fields (list, optional): The fields that should be returned with a query.
            overwrite (bool, optional): Whether to overwrite or append default fields
                                        with user fields. Defaults to False.

        Returns:
            Results: A list of results from the query.
        """

        default_fields = [
            "updated_at",
            "protocols",
            "metadata.description",
            "autonomous_system.name",
            "23.telnet.banner.banner",
            "80.http.get.title",
            "80.http.get.metadata.description",
            "8080.http.get.metadata.description",
            "8888.http.get.metadata.description",
            "443.https.get.metadata.description",
            "443.https.get.title",
            "443.https.tls.certificate.parsed.subject_dn",
            "443.https.tls.certificate.parsed.names",
            "443.https.tls.certificate.parsed.subject.common_name",
            "443.https.tls.certificate.parsed.extensions.subject_alt_name.dns_names",
        ]

        query = kwargs.get("query", "")
        fields = kwargs.get("fields", [])
        overwrite = kwargs.get("overwrite", False)

        index = CensysIPv4(api_id=self.api_user, api_secret=self.api_pass)

        return self._process_search(
            query,
            index,
            self._combine_fields(default_fields, fields, overwrite=overwrite),
        )

    def search_certificates(self, **kwargs) -> Results:
        """
        A method to search the Certificates data set via the API.

        Args:
            query (str): The string search query.
            fields (list, optional): The fields that should be returned with a query.
            overwrite (bool, optional): Whether to overwrite or append default fields
                                        with user fields. Defaults to False.

        Returns:
            Results: A list of results from the query.
        """

        default_fields = [
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
        ]

        query = kwargs.get("query", "")
        fields = kwargs.get("fields", [])
        overwrite = kwargs.get("overwrite", False)

        index = CensysCertificates(api_id=self.api_user, api_secret=self.api_pass)

        return self._process_search(
            query,
            index,
            self._combine_fields(default_fields, fields, overwrite=overwrite),
        )

    def search_websites(self, **kwargs) -> Results:
        """
        A method to search the Websites (Alexa Top 1M) data set via the API.

        Args:
            query (str): The string search query.
            fields (list, optional): The fields that should be returned with a query.
            overwrite (bool, optional): Whether to overwrite or append default fields
                                        with user fields. Defaults to False.

        Returns:
            Results: A list of results from the query.
        """

        default_fields = [
            "443.https.tls.version",
            "alexa_rank",
            "domain",
            "ports",
            "protocols",
            "tags",
            "updated_at",
        ]

        query = kwargs.get("query", "")
        fields = kwargs.get("fields", [])
        overwrite = kwargs.get("overwrite", False)

        index = CensysWebsites(api_id=self.api_user, api_secret=self.api_pass)

        return self._process_search(
            query,
            index,
            self._combine_fields(default_fields, fields, overwrite=overwrite),
        )


class CensysHNRI:
    """
    This class searches the Censys API, check the user's current IP for risks.

    Args:
        api_id (str, optional): The API ID provided by Censys.
        api_secret (str, optional): The API secret provided by Censys.
    """

    HIGH_RISK_DEFINITION: List[str] = ["telnet", "redis", "postgres", "vnc"]
    MEDIUM_RISK_DEFINITION: List[str] = ["ssh", "http", "https"]

    def __init__(self, api_id: str, api_secret: str):
        self.api_id = api_id
        self.api_secret = api_secret

        self.index = CensysIPv4(self.api_id, self.api_secret)

    @staticmethod
    def get_current_ip() -> str:
        """
        Uses ipify.org to get the current IP address.

        Returns:
            str: IP address.
        """

        response = thirdparty.requests.get("https://api.ipify.org?format=json")
        current_ip = response.json().get("ip")
        return current_ip

    def translate_risk(self, protocols: list) -> Tuple[list, list]:
        """
        Interpret protocols to risks.

        Args:
            protocols (list): List of slash divided ports/protocols.

        Returns:
            Tuple[list, list]: Lists of high and medium risks.
        """

        high_risk = []
        medium_risk = []

        for protocol in protocols:
            port, protocol = protocol.split("/")
            string = f"{protocol} on {port}"
            if protocol in self.HIGH_RISK_DEFINITION:
                high_risk.append({"port": port, "protocol": protocol, "string": string})
            elif protocol in self.MEDIUM_RISK_DEFINITION:
                medium_risk.append(
                    {"port": port, "protocol": protocol, "string": string}
                )
            elif protocol == "banner":
                medium_risk.append(
                    {"port": port, "protocol": "unknown protocol", "string": string}
                )
            else:
                medium_risk.append(
                    {"port": port, "protocol": protocol, "string": string}
                )

        return high_risk, medium_risk

    @staticmethod
    def risks_to_string(high_risk: list, medium_risk: list) -> str:
        """
        Risks to printable string.

        Args:
            high_risk (list): Lists of high risks.
            medium_risk (list): Lists of medium risks.

        Raises:
            CensysCLIException: No information/risks found.

        Returns:
            str: Printable string for CLI.
        """

        len_high_risk = len(high_risk)
        len_medium_risk = len(medium_risk)

        if len_high_risk + len_medium_risk == 0:
            raise CensysCLIException

        response = ""
        if len_high_risk > 0:
            response = (
                response
                + "High Risks Found: \n"
                + "\n".join([risk.get("string") for risk in high_risk])
            )
        else:
            response = response + "You don't have any High Risks in your network\n"
        if len_medium_risk > 0:
            response = (
                response
                + "Medium Risks Found: \n"
                + "\n".join([risk.get("string") for risk in medium_risk])
            )
        else:
            response = response + "You don't have any Medium Risks in your network\n"
        return response

    def view_current_ip_risks(self) -> str:
        """
        Gets protocol information for the current IP and returns any risks.

        Returns:
            str: Printable
        """

        current_ip = self.get_current_ip()

        try:
            results = self.index.view(current_ip)
            protocols = results.get("protocols", [])
            high_risk, medium_risk = self.translate_risk(protocols)
            return self.risks_to_string(high_risk, medium_risk)
        except (CensysNotFoundException, CensysCLIException):
            return "No Risks were found on your network"


def search(args):
    """
    search subcommand.

    Args:
        args (Namespace): Argparse Namespace.
    """

    censys_args = {}

    if args.start_page:
        censys_args["start_page"] = args.start_page

    if args.max_pages:
        censys_args["max_pages"] = args.max_pages

    if args.api_id:
        censys_args["api_id"] = args.api_id

    if args.api_secret:
        censys_args["api_secret"] = args.api_secret

    censys = CensysAPISearch(**censys_args)

    search_args = {"query": args.query}

    if args.fields:
        search_args["fields"] = args.fields

    if args.overwrite:
        search_args["overwrite"] = args.overwrite

    indexes = {
        "ipv4": censys.search_ipv4,
        "certs": censys.search_certificates,
        "websites": censys.search_websites,
    }

    index_type = args.index_type or args.query_type

    index_func = indexes[index_type]
    results = index_func(**search_args)

    try:
        censys.write_file(results, file_format=args.format, file_path=args.output)
    except ValueError as error:  # pragma: no cover
        print(f"Error writing log file. Error: {error}")


def hnri(args):
    """
    hnri subcommand.

    Args:
        args (Namespace): Argparse Namespace.
    """

    client = CensysHNRI(args.api_id, args.api_secret)

    risks = client.view_current_ip_risks()

    print(risks)


def cli_config(_):  # pragma: no cover
    """
    config subcommand.

    Args:
        _: Argparse Namespace.
    """

    api_id_prompt = "Censys API ID"
    api_secret_prompt = "Censys API Secret"

    config = get_config()
    api_id = config.get(DEFAULT, "api_id")
    api_secret = config.get(DEFAULT, "api_secret")

    if api_id and api_secret:
        redacted_id = api_id.replace(api_id[:32], 32 * "*")
        redacted_secret = api_secret.replace(api_secret[:28], 28 * "*")
        api_id_prompt = f"{api_id_prompt} [{redacted_id}]"
        api_secret_prompt = f"{api_secret_prompt} [{redacted_secret}]"

    api_id = input(api_id_prompt + ": ").strip() or api_id
    api_secret = input(api_secret_prompt + ": ").strip() or api_secret

    if not (api_id and api_secret):
        print("Please enter valid credentials")
        sys.exit(1)

    try:
        client = CensysAPIBase(api_id, api_secret)
        account = client.account()
        email = account.get("email")

        # Assumes that login was successfully
        config.set(DEFAULT, "api_id", api_id)
        config.set(DEFAULT, "api_secret", api_secret)

        write_config(config)
        print(f"\nSuccessfully authenticated for {email}")
        sys.exit(0)
    except CensysUnauthorizedException:
        print("Failed to authenticate")
        sys.exit(1)


def get_parser() -> argparse.ArgumentParser:
    """
    Gets ArgumentParser for CLI.

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

    parser = argparse.ArgumentParser()
    parser.set_defaults()
    subparsers = parser.add_subparsers()

    # Search Specific Args
    search_parser = subparsers.add_parser(
        "search",
        description="Query Censys Search for resource data by providing a query \
            string, the resource index, and the fields to be returned",
        help="query Censys search",
        parents=[auth],
    )
    search_parser.add_argument(
        "-q",
        "--query",
        type=str,
        required=True,
        help="a string written in Censys Search syntax",
    )

    index_types = ["ipv4", "certs", "websites"]
    index_metavar = "ipv4|certs|websites"
    index_default = "ipv4"
    search_parser.add_argument(
        "--index-type",
        type=str,
        default=index_default,
        choices=index_types,
        metavar=index_metavar,
        help="which resource index to query",
    )
    # Backwards compatibility
    search_parser.add_argument(
        "--query_type",
        type=str,
        default=index_default,
        choices=index_types,
        metavar=index_metavar,
        help=argparse.SUPPRESS,
    )

    search_parser.add_argument(
        "--fields", nargs="+", help="list of index-specific fields"
    )
    search_parser.add_argument(
        "--overwrite",
        action="store_true",
        default=False,
        help="overwrite instead of append fields returned by default \
            with fields provided in the fields argument",
    )
    search_parser.add_argument(
        "-f",
        "--format",
        type=str,
        default="screen",
        metavar="json|csv|screen",
        help="format of output",
    )
    search_parser.add_argument(
        "-o", "--output", type=Path, help="output file path",
    )
    search_parser.add_argument(
        "--start-page", default=1, type=int, help="page number to start from"
    )
    search_parser.add_argument(
        "--max-pages",
        default=1,
        type=int,
        help="maximum number of pages of results to return",
    )
    search_parser.set_defaults(func=search)

    # HNRI Specific Args
    hnri_parser = subparsers.add_parser(
        "hnri",
        description="Home Network Risk Identifier (H.N.R.I.)",
        help="home network risk identifier",
        parents=[auth],
    )
    hnri_parser.set_defaults(func=hnri)

    # Config Specific Args
    config_parser = subparsers.add_parser(
        "config",
        description="Configure Censys API Settings",
        help="configure Censys API settings",
    )
    config_parser.set_defaults(func=cli_config)

    return parser


def main():
    """main cli function"""

    parser = get_parser()

    # Executes by subcommand
    args = parser.parse_args()

    try:
        args.func(args)
    except AttributeError:
        parser.print_help()
        parser.exit()
    except KeyboardInterrupt:  # pragma: no cover
        sys.exit(1)


if __name__ == "__main__":  # pragma: no cover
    main()
