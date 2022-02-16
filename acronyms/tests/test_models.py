import pytest

from acronyms.models import Acronym


@pytest.mark.django_db
def test_string_representation():
    acronym = "cms"
    definition = "Centers for Medicare and Medicaid Services"
    create_by = "test_user"
    approved = True
    value = Acronym.objects.get_or_create(acronym=acronym, definition=definition, create_by=create_by, approved=approved)
    expected = acronym
    actual = str(value[0])
    assert actual == expected


@pytest.mark.django_db
def test_acronym_save_override():
    pass
