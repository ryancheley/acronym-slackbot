import pytest
from django.conf import settings
from django.urls import reverse
from rest_framework.test import APIClient, APIRequestFactory

from acronyms.models import Acronym
from api.views import AcronymViewSet, Events

SLACK_VERIFICATION_TOKEN = getattr(settings, "SLACK_VERIFICATION_TOKEN", None)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "acronym, expected",
    [
        ("aca", 200),
        ("ftf", 404),
    ],
)
def test_get_acronym(acronym, expected):
    Acronym.objects.create(acronym="aca", definition="Affordable Care Act", create_by="lauren", approved=True)
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


def test_get_acronym_verification_success():
    client = APIClient(follow=True)
    url = reverse("api:events")
    data = {"token": SLACK_VERIFICATION_TOKEN, "type": "url_verification"}
    request = client.post(url, data)
    assert request.status_code == 200


# @pytest.mark.django_db
# def test_slash_function_count_with_zero_results():
#     client = APIClient()
#     client.login(username="lauren", password="secret")
#     request = client.post("/api/slack/count/")
#     actual = request.data
#     expected = "There are 0. Here is a random one None"
#     assert actual == expected


# @pytest.mark.django_db
# def test_slash_function_count_with_non_zero_results():
#     Acronym.objects.create(acronym="aca", definition="Affordable Care Act", create_by="lauren", approved=True)
#     client = APIClient()
#     client.login(username="lauren", password="secret")
#     request = client.post("/api/slack/count/")
#     actual = request.data
#     expected = "There are 1. Here is a random one aca"
#     assert actual == expected
