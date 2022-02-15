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

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

SLACK_VERIFICATION_TOKEN = getattr(settings, "SLACK_VERIFICATION_TOKEN", None)
SLACK_BOT_USER_TOKEN = getattr(settings, "SLACK_BOT_USER_TOKEN", None)
CONFLUENCE_LINK = getattr(settings, "CONFLUENCE_LINK", None)
client = slack.WebClient(SLACK_BOT_USER_TOKEN, ssl=ssl_context)


class AcronymViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AcronymSerializer
    queryset = Acronym.objects.all()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        print(self.kwargs["acronym"])
        acronym = self.kwargs["acronym"]
        obj = get_object_or_404(queryset, acronym__iexact=acronym)

        return obj


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
                confluence_link = CONFLUENCE_LINK + f'/dosearchsite.action?cql=siteSearch+~+"{text}"'
                message = f"I'm sorry <@{user}> I don't know what *{text.upper()}* is :shrug:. \
                    Try checking <{confluence_link}|Confluence>"

            if user != "U031T0UHLH1":
                client.chat_postMessage(
                    blocks=[{"type": "section", "text": {"type": "mrkdwn", "text": message}}], channel=channel
                )
                return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_200_OK)
