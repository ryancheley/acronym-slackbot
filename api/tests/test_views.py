import pytest
from django.conf import settings
from django.urls import reverse
from rest_framework.test import APIClient

from acronyms.models import Acronym

SLACK_VERIFICATION_TOKEN = getattr(settings, "SLACK_VERIFICATION_TOKEN", None)


@pytest.mark.django_db
def test_get_acronym_success():
    Acronym.objects.create(acronym="aca", definition="Affordable Care Act", create_by="lauren", approved=True)
    url = reverse("api:acronym-detail", kwargs={"acronym": "aca"})
    client = APIClient()
    request = client.get(url)
    assert request.status_code == 200


@pytest.mark.django_db
def test_get_acronym_failure():
    Acronym.objects.create(acronym="aca", definition="Affordable Care Act", create_by="lauren", approved=True)
    url = reverse("api:acronym-detail", kwargs={"acronym": "ftf"})
    client = APIClient()
    request = client.get(url)
    assert request.status_code == 404


def test_get_acronym_verification_failure():
    client = APIClient()
    url = reverse("api:events")
    request = client.post(url)
    assert request.status_code == 403


def test_get_acronym_verification_success():
    client = APIClient()
    url = reverse("api:events")
    data = {"token": SLACK_VERIFICATION_TOKEN, "type": "url_verification", "user": "ryan"}
    request = client.post(url, data)
    assert request.status_code == 200


@pytest.mark.django_db
def test_slash_function_count_with_zero_results():
    client = APIClient()
    client.login(username="lauren", password="secret")
    request = client.post("/api/slack/count/")
    actual = request.data
    expected = "There are 0. Here is a random one None"
    assert actual == expected


@pytest.mark.django_db
def test_slash_function_count_with_non_zero_results():
    Acronym.objects.create(acronym="aca", definition="Affordable Care Act", create_by="lauren", approved=True)
    client = APIClient()
    client.login(username="lauren", password="secret")
    request = client.post("/api/slack/count/")
    actual = request.data
    expected = "There are 1. Here is a random one aca"
    assert actual == expected
