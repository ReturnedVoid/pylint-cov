"""Utilities for analyzing pylint output and determining which
pylint:disable(s) are useless
"""
import re
import subprocess

PYLINT_READABLE_ERROR_REGEX = re.compile(r'\(([^(]+?)\)$', re.M)


def _get_disabled_issues(content: str) -> set:
    lines = content.split('\n')

    styles = ('#pylint:disable=', '# pylint:disable=')

    disabled = []
    for line in lines:
        if line.startswith('#'):
            for style in styles:
                split = line.split(style)
                if len(split) > 1:
                    errors = split[1]
                    for error in errors.split(','):
                        disabled.append(error.strip())

    return set(disabled)


def _get_content_without_comments(string: str) -> str:
    out = ''
    for line in string.split('\n'):
        if line.startswith('#'):
            out += '\n'
        else:
            out += line + '\n'

    return out


def _get_pylint_issues(content) -> set:
    stripped_content = _get_content_without_comments(content)
    proc = subprocess.run(
        ['pylint', '--from-stdin', 'some.py'],
        input=stripped_content, encoding='utf8', text=True, capture_output=True
    )

    return set(
        PYLINT_READABLE_ERROR_REGEX.findall(proc.stdout)
    )


def get_useless_disables(path: str) -> set:
    with open(path) as file:
        content = file.read()

    return _get_disabled_issues(content) - _get_pylint_issues(content)
