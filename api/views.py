import ssl

import requests
import slack
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from acronyms.models import Acronym

from .serializers import AcronymSerializer
from .utils import acronym_checker, string_split

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

SLACK_VERIFICATION_TOKEN = getattr(settings, "SLACK_VERIFICATION_TOKEN", None)
SLACK_BOT_USER_TOKEN = getattr(settings, "SLACK_BOT_USER_TOKEN", None)
CONFLUENCE_LINK = getattr(settings, "CONFLUENCE_LINK", None)
client = slack.WebClient(SLACK_BOT_USER_TOKEN, ssl=ssl_context)


class AcronymViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AcronymSerializer
    queryset = Acronym.objects.filter(approved=True)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        print(self.kwargs["acronym"])
        acronym = self.kwargs["acronym"]
        obj = get_object_or_404(queryset, acronym__iexact=acronym)

        return obj


class CountAcronyms(APIView):
    def post(self, request, *args, **kwargs):
        total_acronymns = Acronym.objects.count()
        random_acronym = Acronym.objects.order_by("?").first()
        message = f"There are {total_acronymns}. Here is a random one {random_acronym}"
        return Response(data=message, status=status.HTTP_200_OK)


class AddAcronym(APIView):
    def post(self, request, *args, **kwargs):
        request_data = string_split(request.data["text"])
        acronym = request_data[0]
        channel = request.data["channel_id"]
        try:
            acronym_checker(acronym=acronym)
        except AttributeError:
            message = f"Acronyms need to be 8 characters or fewer. The acronym '{acronym}' is {len(acronym)}. Please try again."
            client.chat_postMessage(blocks=[{"type": "section", "text": {"type": "mrkdwn", "text": message}}], channel=channel)
            return Response(status=status.HTTP_201_CREATED)
        except TypeError:
            message = "The format of the acronym add needs to be 'acronym: definition'."
            message += "'\nFor example:\n\t*example: this is an example.*\nPlease try again."
            client.chat_postMessage(blocks=[{"type": "section", "text": {"type": "mrkdwn", "text": message}}], channel=channel)
            return Response(status=status.HTTP_201_CREATED)
        definition = request_data[1]
        check_for_acronym = Acronym.objects.filter(acronym=acronym).exists()
        if not check_for_acronym and acronym and definition:
            user = request.data["user_name"]
            message = f"The acronym *{acronym.upper()}* with definition '{definition}' has been added!"
            client.chat_postMessage(blocks=[{"type": "section", "text": {"type": "mrkdwn", "text": message}}], channel=channel)
            record = Acronym.objects.create(
                acronym=acronym,
                definition=definition,
                create_by=user,
                approved=False,
            )
            record.save()
            return Response(status=status.HTTP_201_CREATED)
        elif not acronym or not definition:
            message = "You have entered the data incorrectly!"
            client.chat_postMessage(blocks=[{"type": "section", "text": {"type": "mrkdwn", "text": message}}], channel=channel)
            return Response(status=status.HTTP_200_OK)
        else:
            message = f"The acronym {acronym} with definition {definition} already exists!"
            client.chat_postMessage(blocks=[{"type": "section", "text": {"type": "mrkdwn", "text": message}}], channel=channel)
            return Response(status=status.HTTP_200_OK)

            # return Response(status=status.HTTP_409_CONFLICT)


class Events(APIView):
    def post(self, request, *args, **kwargs):

        slack_message = request.data

        if slack_message.get("token") != SLACK_VERIFICATION_TOKEN:
            return Response(status=status.HTTP_403_FORBIDDEN)

        # verification challenge
        if slack_message.get("type") == "url_verification":
            return Response(data=slack_message, status=status.HTTP_200_OK)
        # greet bot
        if "event" in slack_message:
            event_message = slack_message.get("event")

            # ignore bot's own message
            if event_message.get("subtype"):
                return Response(status=status.HTTP_200_OK)

            # process user's message
            user = event_message.get("user")
            text = event_message.get("text")
            channel = event_message.get("channel")
            url = f"https://slackbot.ryancheley.com/api/{text}/"
            response = requests.get(url).json()
            definition = response.get("definition")
            if definition:
                message = f"The acronym '{text.upper()}' means: {definition}"
            else:
                confluence = CONFLUENCE_LINK + f'/dosearchsite.action?cql=siteSearch+~+"{text}"'
                confluence_link = f"<{confluence}|Confluence>"
                message = f"I'm sorry <@{user}> I don't know what *{text.upper()}* is :shrug:. Try checking {confluence_link}."

            if user != "U031T0UHLH1":
                client.chat_postMessage(
                    blocks=[{"type": "section", "text": {"type": "mrkdwn", "text": message}}], channel=channel
                )
                return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_200_OK)
