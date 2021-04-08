"""Main module for the script."""
from .cli import parse_cli_args
from .script import get_issues


def main():
    """Define main entry point."""
    args = parse_cli_args()

    for file, issues in get_issues(file=args.file, directory=args.directory):
        if issues:
            print('{}: {}'.format(file, issues))
