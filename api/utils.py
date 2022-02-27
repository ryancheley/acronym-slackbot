import ssl

import requests
import slack
from django.conf import settings
from rest_framework import status

from acronyms.models import Acronym

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

SLACK_VERIFICATION_TOKEN = getattr(settings, "SLACK_VERIFICATION_TOKEN", None)
SLACK_BOT_USER_TOKEN = getattr(settings, "SLACK_BOT_USER_TOKEN", None)
CONFLUENCE_LINK = getattr(settings, "CONFLUENCE_LINK", None)
client = slack.WebClient(SLACK_BOT_USER_TOKEN, ssl=ssl_context)


def process_user_message(text: str, user: str):
    url = f"https://slackbot.ryancheley.com/api/{text}/"
    response = requests.get(url).json()
    definition = response.get("definition")
    if definition:
        message = f"The acronym '{text.upper()}' means: {definition}"
    else:
        confluence = CONFLUENCE_LINK + f'/dosearchsite.action?cql=siteSearch+~+"{text}"'
        confluence_link = f"<{confluence}|Confluence>"
        message = f"I'm sorry <@{user}> I don't know what *{text.upper()}* is :shrug:. Try checking {confluence_link}."

    return message


def format_checker(text: str):
    request_data = string_split(text)
    acronym = request_data[0]
    try:
        acronym_length_checker(acronym=acronym)
    except AttributeError:
        message = f"Acronyms need to be 8 characters or fewer. The acronym '{acronym}' is {len(acronym)}. Please try again."
        response_status = status.HTTP_205_RESET_CONTENT
        return message, response_status
    except TypeError:
        message = "The format of the acronym add needs to be 'acronym: definition'."
        message += "'\nFor example:\n\t*example: this is an example.*\nPlease try again."
        response_status = status.HTTP_205_RESET_CONTENT
        return message, response_status
    definition = request_data[1]
    check_for_acronym = Acronym.objects.filter(acronym=acronym).exists()
    if not check_for_acronym and acronym and definition:
        message = f"The acronym *{acronym.upper()}* with definition '{definition}' has been added!"
        response_status = status.HTTP_201_CREATED
    else:
        message = f"The acronym {acronym} with definition {definition} already exists!"
        response_status = status.HTTP_205_RESET_CONTENT
    return message, response_status


def string_split(input: str):
    data = input.split(":")
    if len(data) == 2:
        acronym = data[0]
        definition = data[1].strip()
        return (acronym, definition)
    else:
        return (None, None)


def acronym_length_checker(acronym: str):
    if len(acronym) > 8:
        raise AttributeError
    else:
        pass
