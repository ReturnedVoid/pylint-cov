"""Script logic."""
import os
from .analyze import get_useless_disables


def get_issues(file=None, directory=None):
    if file:
        yield (file, get_useless_disables(file))

    else:
        if directory:
            source_dir = directory
        else:
            source_dir = os.getcwd()

        for dirpath, _, filenames in os.walk(source_dir):
            for filename in filenames:
                if filename.endswith('.py'):
                    path = os.path.join(dirpath, filename)
                    yield (path, get_useless_disables(path))
