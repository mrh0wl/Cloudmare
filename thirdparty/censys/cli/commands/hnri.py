"""Censys HNRI CLI."""
import argparse
import sys
import webbrowser
from typing import Any, List, Optional, Tuple

import requests
from rich import box
from rich.table import Table

from censys.cli.utils import console
from censys.common.exceptions import CensysCLIException, CensysNotFoundException
from censys.search import CensysHosts


class CensysHNRI:
    """Searches the Censys API for the user's current IP to scan for risks."""

    HIGH_RISK_DEFINITION: List[str] = ["TELNET", "REDIS", "POSTGRES", "VNC"]
    MEDIUM_RISK_DEFINITION: List[str] = ["SSH", "HTTP", "HTTPS"]

    def __init__(self, api_id: Optional[str] = None, api_secret: Optional[str] = None):
        """Inits CensysHNRI.

        Args:
            api_id (str): Optional; The API ID provided by Censys.
            api_secret (str): Optional; The API secret provided by Censys.
        """
        self.index = CensysHosts(api_id, api_secret)

    @staticmethod
    def get_current_ip() -> str:
        """Uses ipify.org to get the current IP address.

        Returns:
            str: IP address.
        """
        response = requests.get("https://api.ipify.org?format=json")
        current_ip = str(response.json().get("ip"))
        return current_ip

    def translate_risk(self, services: List[dict]) -> Tuple[List[dict], List[dict]]:
        """Interpret protocols to risks.

        Args:
            services (list): List of services.

        Returns:
            Tuple[list, list]: Lists of high and medium risks.
        """
        high_risk = []
        medium_risk = []

        for service in services:
            service_name = service.get("service_name")
            if service_name in self.HIGH_RISK_DEFINITION:
                high_risk.append(service)
            elif service_name in self.MEDIUM_RISK_DEFINITION:
                medium_risk.append(service)
            else:
                medium_risk.append(service)

        return high_risk, medium_risk

    def make_risks_into_table(self, title: str, risks: List[dict]) -> Table:
        """Creates a table of risks.

        Args:
            title (str): Title of the table.
            risks (list): List of risks.

        Returns:
            Table: Table of risks.
        """
        table = Table("Port", "Service Name", title=title, box=box.SQUARE)
        for risk in risks:
            table.add_row(str(risk.get("port")), risk.get("service_name"))
        return table

    def risks_to_string(self, high_risks: list, medium_risks: list) -> List[Any]:
        """Risks to printable string.

        Args:
            high_risks (list): Lists of high risks.
            medium_risks (list): Lists of medium risks.

        Raises:
            CensysCLIException: No information/risks found.

        Returns:
            list: Printable objects for CLI.
        """
        len_high_risk = len(high_risks)
        len_medium_risk = len(medium_risks)

        if len_high_risk + len_medium_risk == 0:
            raise CensysCLIException

        response: List[Any] = []
        if len_high_risk > 0:
            response.append(
                self.make_risks_into_table(
                    ":exclamation: High Risks Found",
                    high_risks,
                )
            )
        else:
            response.append("You don't have any High Risks in your network\n")
        if len_medium_risk > 0:
            response.append(
                self.make_risks_into_table(
                    ":grey_exclamation: Medium Risks Found",
                    medium_risks,
                )
            )
        else:
            response.append("You don't have any Medium Risks in your network\n")
        return response

    def view_current_ip_risks(self):
        """Gets protocol information for the current IP and returns any risks."""
        current_ip = self.get_current_ip()

        try:
            console.print(f"Searching for information on {current_ip}...")
            results = self.index.view(current_ip)
            services = results.get("services", [])
            high_risk, medium_risk = self.translate_risk(services)
            for res in self.risks_to_string(high_risk, medium_risk):
                console.print(res)
            console.print(
                f"\nFor more information, please visit: https://search.censys.io/hosts/{current_ip}"
            )
        except (CensysNotFoundException, CensysCLIException):
            console.print(
                "[green]:white_check_mark: No Risks were found on your network[/green]"
            )


def cli_hnri(args: argparse.Namespace):
    """HNRI subcommand.

    Args:
        args (Namespace): Argparse Namespace.
    """
    if args.open:
        webbrowser.open("https://search.censys.io/me")
        sys.exit(0)

    client = CensysHNRI(args.api_id, args.api_secret)

    client.view_current_ip_risks()


def include(parent_parser: argparse._SubParsersAction, parents: dict):
    """Include this subcommand into the parent parser.

    Args:
        parent_parser (argparse._SubParsersAction): Parent parser.
        parents (dict): Parent arg parsers.
    """
    hnri_parser = parent_parser.add_parser(
        "hnri",
        description="Home Network Risk Identifier (H.N.R.I.)",
        help="home network risk identifier",
        parents=[parents["auth"]],
    )
    hnri_parser.add_argument(
        "-O",
        "--open",
        action="store_true",
        help="open your IP in browser",
    )
    hnri_parser.set_defaults(func=cli_hnri)
