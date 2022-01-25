"""Censys config CLI."""
import argparse
import os
import sys

from rich.prompt import Confirm, Prompt

from censys.cli.utils import console
from censys.common.config import DEFAULT, get_config, write_config
from censys.common.exceptions import CensysUnauthorizedException
from censys.search.v2.api import CensysSearchAPIv2


def cli_config(_: argparse.Namespace):  # pragma: no cover
    """Config subcommand.

    Args:
        _: Argparse Namespace.
    """
    api_id_prompt = "Censys API ID"
    api_secret_prompt = "Censys API Secret"

    config = get_config()
    api_id = config.get(DEFAULT, "api_id")
    api_secret = config.get(DEFAULT, "api_secret")

    api_id_env = os.getenv("CENSYS_API_ID")
    api_secret_env = os.getenv("CENSYS_API_SECRET")

    if api_id_env is not None or api_secret_env is not None:
        console.print(
            "Please note environment variables (CENSYS_API_ID & CENSYS_API_SECRET) "
            "will take priority over configured credentials."
        )
        api_id = api_id_env or api_id
        api_secret = api_secret_env or api_secret

    if api_id and api_secret:
        redacted_id = api_id.replace(api_id[:32], 32 * "*")
        redacted_secret = api_secret.replace(api_secret[:28], 28 * "*")
        api_id_prompt = f"{api_id_prompt} [cyan]({redacted_id})[/cyan]"
        api_secret_prompt = f"{api_secret_prompt} [cyan]({redacted_secret})[/cyan]"

    api_id = Prompt.ask(api_id_prompt, console=console) or api_id
    api_secret = Prompt.ask(api_secret_prompt, console=console) or api_secret

    if not (api_id and api_secret):
        console.print("Please enter valid credentials")
        sys.exit(1)

    api_id = api_id.strip()
    api_secret = api_secret.strip()

    color = Confirm.ask(
        "Do you want color output?", default=True, show_default=False, console=console
    )
    config.set(DEFAULT, "color", "auto" if color else "")

    try:
        client = CensysSearchAPIv2(api_id, api_secret)
        account = client.account()
        email = account.get("email")
        console.print(f"\nSuccessfully authenticated for {email}")

        # Assumes that login was successfully
        config.set(DEFAULT, "api_id", api_id)
        config.set(DEFAULT, "api_secret", api_secret)

        write_config(config)
        sys.exit(0)
    except CensysUnauthorizedException:
        console.print("Failed to authenticate")
        sys.exit(1)
    except PermissionError as e:
        console.print(e)
        console.print(
            "Cannot write config file to directory. "
            + "Please set the `CENSYS_CONFIG_PATH` environmental variable to a writeable location."
        )
        sys.exit(1)


def include(parent_parser: argparse._SubParsersAction, parents: dict):
    """Include this subcommand into the parent parser.

    Args:
        parent_parser (argparse._SubParsersAction): Parent parser.
        parents (dict): Parent arg parsers.
    """
    config_parser = parent_parser.add_parser(
        "config",
        description="Configure Censys Search API Settings",
        help="configure Censys search API settings",
    )
    config_parser.set_defaults(func=cli_config)
