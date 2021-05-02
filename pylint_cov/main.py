"""Main module for the script."""
import logging
from .cli import parse_cli_args
from .script import get_issues


def main():
    """Define main entry point."""
    args = parse_cli_args()

    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=level, format='%(message)s')

    for file, issues in get_issues(file=args.file, directory=args.directory):
        if issues:
            logging.info('%s: %s', file, issues)
