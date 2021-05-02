"""Command Line Interface."""
import argparse


def parse_cli_args():
    parser = argparse.ArgumentParser(
        description='Script that finds out useless pylint:disable.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('-f', '--file', help='file (path) to process')
    parser.add_argument('-d', '--directory',
                        help='directory to process files in')

    return parser.parse_args()
