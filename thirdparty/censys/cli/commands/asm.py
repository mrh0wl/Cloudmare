"""Censys ASM CLI."""
import argparse
import json
import sys

from rich.prompt import Confirm, Prompt

from censys.asm.seeds import SEED_TYPES, Seeds
from censys.cli.utils import console
from censys.common.config import DEFAULT, get_config, write_config
from censys.common.exceptions import CensysUnauthorizedException


def cli_asm_config(_: argparse.Namespace):  # pragma: no cover
    """Config asm subcommand.

    Args:
        _: Argparse Namespace.
    """
    api_key_prompt = "Censys ASM API Key"

    config = get_config()
    api_key = config.get(DEFAULT, "asm_api_key")

    if api_key:
        key_len = len(api_key) - 4
        redacted_api_key = api_key.replace(api_key[:key_len], key_len * "*")
        api_key_prompt = f"{api_key_prompt} [cyan]({redacted_api_key})[/cyan]"

    api_key = Prompt.ask(api_key_prompt, console=console) or api_key

    if not api_key:
        console.print("Please enter valid credentials")
        sys.exit(1)

    color = Confirm.ask(
        "Do you want color output?", default=True, show_default=False, console=console
    )
    config.set(DEFAULT, "color", "auto" if color else "")

    try:
        # Assumes that login was successfully
        config.set(DEFAULT, "asm_api_key", api_key)

        write_config(config)
        console.print("\nSuccessfully configured credentials")
        sys.exit(0)
    except CensysUnauthorizedException:
        console.print("Failed to authenticate")
        sys.exit(1)


def cli_add_seeds(args: argparse.Namespace):
    """Add seed subcommand.

    Args:
        args (Namespace): Argparse Namespace.
    """
    if args.input_file:
        if args.input_file == "-":
            data = sys.stdin.read()
        else:
            with open(args.input_file) as f:
                data = f.read()
    else:
        data = args.json
    try:
        seeds = json.loads(data)
    except json.decoder.JSONDecodeError as e:
        console.print(f"Invalid json {e}")
        sys.exit(1)

    seeds_to_add = []
    for seed in seeds:
        if isinstance(seed, dict):
            if "type" not in seed:
                seed["type"] = args.default_type
        elif isinstance(seed, str):
            seed = {"value": seed, "type": args.default_type}
        else:
            console.print(f"Invalid seed {seed}")
            sys.exit(1)
        if "label" not in seed:
            seed["label"] = args.label_all
        seeds_to_add.append(seed)

    s = Seeds(args.api_key)
    to_add_count = len(seeds_to_add)
    res = s.add_seeds(seeds_to_add)
    added_seeds = res["addedSeeds"]
    added_count = len(added_seeds)
    if not added_count:
        console.print("No seeds were added. (Run with -v to get more info)")
        if not args.verbose:
            sys.exit(1)
    else:
        console.print(f"Added {added_count} seeds.")
    if added_count < to_add_count:
        console.print(f"Seeds not added: {to_add_count - added_count}")
        if args.verbose:  # pragma: no cover
            console.print(
                "The following seed(s) were not able to be added as they already exist or are reserved."
            )
            for seed in seeds_to_add:
                if not any([s for s in added_seeds if seed["value"] == s["value"]]):
                    console.print_json(seed)


def include(parent_parser: argparse._SubParsersAction, parents: dict):
    """Include this subcommand into the parent parser.

    Args:
        parent_parser (argparse._SubParsersAction): Parent parser.
        parents (dict): Parent arg parsers.
    """
    asm_parser = parent_parser.add_parser(
        "asm", description="Interact with the Censys ASM API", help="interact with ASM"
    )
    asm_subparser = asm_parser.add_subparsers()

    # Add config command
    config_parser = asm_subparser.add_parser(
        "config",
        description="Configure Censys ASM API Settings",
        help="configure Censys ASM API settings",
    )
    config_parser.set_defaults(func=cli_asm_config)

    # Add seed command
    add_parser = asm_subparser.add_parser(
        "add-seeds",
        description="Add seeds to ASM",
        help="add seeds",
        parents=[parents["asm_auth"]],
    )
    add_parser.add_argument(
        "--default-type",
        help="type of the seed(s) if type is not already provided (default: %(default)s)",
        choices=SEED_TYPES,
        default="IP_ADDRESS",
    )
    add_parser.add_argument(
        "--label-all",
        help='label to apply to all seeds (default: "")',
        type=str,
        default="",
    )
    add_parser.add_argument(
        "-v",
        "--verbose",
        help="verbose output",
        action="store_true",
    )
    seeds_group = add_parser.add_mutually_exclusive_group(required=True)
    seeds_group.add_argument(
        "--input-file",
        "-i",
        help="input file name containing valid json seeds (use - for stdin)",
        type=str,
    )
    seeds_group.add_argument(
        "--json", "-j", help="input string containing valid json seeds", type=str
    )
    add_parser.set_defaults(func=cli_add_seeds)
