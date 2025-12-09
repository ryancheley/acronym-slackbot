import pytest
from django.conf import settings
from django.urls import reverse
from rest_framework.test import APIRequestFactory

from acronyms.models import Acronym
from api.views import AcronymViewSet, CountAcronyms, Events


SLACK_VERIFICATION_TOKEN = getattr(settings, "SLACK_VERIFICATION_TOKEN", None)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "acronym, expected",
    [
        ("aca", 200),
        ("ftf", 404),
        ("ftq", 404),
    ],
)
def test_get_acronym(acronym, expected):
    Acronym.objects.create(acronym="aca", definition="Affordable Care Act", create_by="lauren", approved=True)
    Acronym.objects.create(acronym="ftf", definition="Face to Face", create_by="lauren", approved=False)
    url = reverse("api:acronym-detail", kwargs={"acronym": acronym})
    factory = APIRequestFactory()
    view = AcronymViewSet.as_view({"get": "retrieve"})
    request = factory.get(url)
    response = view(request, acronym=acronym)
    assert response.status_code == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        ({"token": SLACK_VERIFICATION_TOKEN, "type": "url_verification"}, 200),
        (None, 403),
    ],
)
def test_get_acronym_verification(data, expected):
    url = reverse("api:events")
    factory = APIRequestFactory()
    view = Events.as_view()
    request = factory.post(url, data=data)
    response = view(request)
    assert response.status_code == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        (True, "There are 1. Here is a random one aca"),
        (False, "There are 0. Here is a random one None"),
    ],
)
@pytest.mark.django_db
def test_slash_function_count(data, expected):
    if data:
        Acronym.objects.create(acronym="aca", definition="Affordable Care Act", create_by="lauren", approved=True)
    url = reverse("api:count-acronyms")
    factory = APIRequestFactory()
    view = CountAcronyms.as_view()
    request = factory.post(url)
    response = view(request)
    assert response.data == expected
