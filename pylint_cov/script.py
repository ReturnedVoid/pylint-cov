"""Script logic."""
import logging
import os
from typing import Generator

from .analyze import get_useless_disables


def get_issues(file: str = None,
               directory: str = None) -> Generator[tuple, None, None]:
    """Get all issues.

    :param file: if specified, it will be analyzed directly
    :param directory: if specified, all .py files from this directory will be
        analyzed
    """
    if file:
        logging.debug('Finding useless disables in "%s"', file)
        yield (file, get_useless_disables(file))

    else:
        if directory:
            source_dir = directory
        else:
            logging.debug('Using the current directory')
            source_dir = os.getcwd()

        for dirpath, _, filenames in os.walk(source_dir):
            for filename in filenames:
                if filename.endswith('.py'):
                    path = os.path.join(dirpath, filename)
                    logging.debug('Finding useless disables in "%s"', path)
                    yield (path, get_useless_disables(path))
