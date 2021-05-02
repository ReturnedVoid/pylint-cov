import tempfile
from pylint_cov import analyze


def test_get_useless_disables_empty_file_no_useless_disables():
    with tempfile.NamedTemporaryFile(mode='w+') as tmp_file:
        tmp_file.write('')
        tmp_file.flush()
        assert analyze.get_useless_disables(tmp_file.name) == set()


def test_get_useless_disables_one_useless_disable():
    with tempfile.NamedTemporaryFile(mode='w+') as tmp_file:
        tmp_file.write("# pylint:disable=no-member")
        tmp_file.flush()
        assert analyze.get_useless_disables(tmp_file.name) == {'no-member', }


def test_get_useless_disables_one_useless_disable_different_style():
    with tempfile.NamedTemporaryFile(mode='w+') as tmp_file:
        tmp_file.write("#pylint:disable=no-member")
        tmp_file.flush()
        assert analyze.get_useless_disables(tmp_file.name) == {'no-member', }


def test_get_useless_disables_couple_problems_in_one_line():
    with tempfile.NamedTemporaryFile(mode='w+') as tmp_file:
        tmp_file.write("# pylint:disable=no-member, other")
        tmp_file.flush()
        assert analyze.get_useless_disables(
            tmp_file.name
        ) == {'no-member', 'other', }


def test_get_useless_disables_couple_problems_on_different_lines():
    with tempfile.NamedTemporaryFile(mode='w+') as tmp_file:
        tmp_file.write(
            '#pylint:disable=no-member,other\nSome text \n#pylint:disable=third\n'
            '#pylint:disable=four,five,six'
        )
        tmp_file.flush()
        assert analyze.get_useless_disables(
            tmp_file.name
        ) == {'no-member', 'other', 'third', 'four', 'five', 'six', }


def test_get_useless_disables_duplicates_excluded():
    with tempfile.NamedTemporaryFile(mode='w+') as tmp_file:
        tmp_file.write(
            '#pylint:disable=one,one,two\n'
            '#pylint:disable=one,three'
        )
        tmp_file.flush()
        assert analyze.get_useless_disables(
            tmp_file.name
        ) == {'one', 'two', 'three'}


def test_get_useless_disables_one_issue_disabled():
    with tempfile.NamedTemporaryFile(mode='w+') as tmp_file:
        tmp_file.write(
            '# pylint:disable=missing-module-docstring\n'
            'pass'
        )
        tmp_file.flush()
        assert analyze.get_useless_disables(tmp_file.name) == set()


def test_get_useless_disables_one_useless_based_on_pylint():
    with tempfile.NamedTemporaryFile(mode='w+') as tmp_file:
        tmp_file.write(
            '"""Docstring."""\n'
            '# pylint:disable=missing-module-docstring\n'
            'pass'
        )
        tmp_file.flush()
        assert analyze.get_useless_disables(tmp_file.name) == {
            'missing-module-docstring',
        }


def test_get_useless_disables_couple_useless_based_on_pylint():
    with tempfile.NamedTemporaryFile(mode='w+') as tmp_file:
        tmp_file.write(
            '# pylint:disable=missing-module-docstring, undefined-variable, invalid-name\n\n\n'
            'def main():\n'
            '    call(lambda x: 1)\n\n\n'
            '# pylint:disable=empty-docstring\n\n\n'
        )
        tmp_file.flush()
        assert analyze.get_useless_disables(tmp_file.name) == {
            'invalid-name', 'empty-docstring'
        }
