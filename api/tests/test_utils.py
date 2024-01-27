from random import randint

import pytest
from django.conf import settings
from rest_framework import status

from acronyms.models import Acronym
from api.utils import (
    acronym_length_checker,
    format_checker,
    process_user_message,
    string_split,
)

bad_search_term = "cad"
CONFLUENCE_LINK = getattr(settings, "CONFLUENCE_LINK", None)
confluence = CONFLUENCE_LINK + f'articles?query=%7B{bad_search_term}%7D'
confluence_link = f"<{confluence}|YouTrack>"


@pytest.mark.django_db
@pytest.mark.parametrize(
    "acronym, user ,expected",
    [
        ("aca", "ryan", "The acronym 'ACA' means: Affordable Care Act"),
        (
            bad_search_term,
            "ryan",
            f"I'm sorry <@ryan> I don't know what *{bad_search_term.upper()}* is :shrug:. Try checking {confluence_link}.",
        ),
    ],
)
def test_process_user_message_acronym_exists(acronym, user, expected):
    Acronym.objects.create(acronym="aca", definition="Affordable Care Act", create_by="lauren", approved=True)
    actual = process_user_message(acronym, user)
    assert actual == expected


@pytest.mark.django_db
@pytest.mark.parametrize(
    "string_to_check,expected",
    [
        ("test: test", ("The acronym *TEST* with definition 'test' has been added!", status.HTTP_201_CREATED)),
        (
            "xxxxxxxxxxxx: definition",
            (
                "Acronyms need to be 8 characters or fewer. The acronym 'xxxxxxxxxxxx' is 12. Please try again.",
                status.HTTP_205_RESET_CONTENT,
            ),
        ),
        (
            "xxxxxxxxxxxx",
            (
                "The format of the acronym add needs to be 'acronym: definition'.\
'\nFor example:\n\t*example: this is an example.*\nPlease try again.",
                status.HTTP_205_RESET_CONTENT,
            ),
        ),
        (
            "aca: aca definition",
            ("The acronym aca with definition aca definition already exists!", status.HTTP_205_RESET_CONTENT),
        ),
    ],
)
def test_format_checker(string_to_check, expected):
    Acronym.objects.create(acronym="aca", definition="Affordable Care Act", create_by="lauren", approved=True)

    actual = format_checker(string_to_check)
    assert actual == expected


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
        acronym_length_checker(acronym)


def test_check_acronym_checker_len_less_than_or_equal_to_8():
    acronym = randint(1, 8) * "x"
    actual = acronym_length_checker(acronym)
    assert actual is None
