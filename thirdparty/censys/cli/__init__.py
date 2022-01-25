#!/usr/bin/env python3
"""Interact with the Censys Search API through the command line."""
import sys

from .args import get_parser
from censys.common.version import __version__


def main():
    """Main cli function."""
    parser = get_parser()

    # Executes by subcommand
    args = parser.parse_args()

    if args.version:
        print(f"Censys Python Version: {__version__}")
        sys.exit(0)

    try:
        args.func(args)
    except KeyboardInterrupt:  # pragma: no cover
        sys.exit(1)


if __name__ == "__main__":  # pragma: no cover
    main()
