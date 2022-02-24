from random import randint

import pytest

from api.utils import acronym_checker, string_split


def test_check_string_split_len_equal_2():
    test_string = "test: this is a test"
    actual = string_split(test_string)
    expected = ("test", "this is a test")
    assert actual == expected


def test_check_string_split_len_not_equal_2():
    test_string = "test this is a test"
    actual = string_split(test_string)
    expected = (None, None)
    assert actual == expected


def test_check_acronym_checker_len_greater_than_8():
    acronym = randint(9, 255) * "x"
    with pytest.raises(AttributeError):
        acronym_checker(acronym)


def test_check_acronym_checker_len_less_than_or_equal_to_8():
    acronym = randint(1, 8) * "x"
    actual = acronym_checker(acronym)
    assert actual is None
