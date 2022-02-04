import pytest

from acronyms.models import Acronym


@pytest.mark.django_db
def test_string_representation():
    acronym = "cms"
    definition = "Centers for Medicare and Medicaid Services"
    value = Acronym.objects.get_or_create(acronym=acronym, definition=definition)
    expected = acronym
    actual = str(value[0])
    assert actual == expected


@pytest.mark.django_db
def test_acronym_save_override():
    pass
