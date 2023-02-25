import ssl
from datetime import datetime

import slack
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from acronyms.models import Acronym

from .serializers import AcronymSerializer
from .utils import format_checker, process_user_message, string_split

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
    def post(self, request, *args, **kwargs):  # pragma: no cover
        request_data = request.data["text"]
        channel = request.data["channel_id"]
        message, response_status = format_checker(request_data)
        blocks = [{"type": "section", "text": {"type": "mrkdwn", "text": message}}]
        client.chat_postMessage(blocks=blocks, channel=channel)
        if response_status == status.HTTP_201_CREATED:
            acronym, definition = string_split(request_data)
            user = request.data["user_name"]
            record = Acronym.objects.create(
                acronym=acronym, definition=definition, create_by=user, create_date=datetime.now(), approved=False
            )
            record.save()
        return Response(status=response_status)


class Events(APIView):
    def post(self, request, *args, **kwargs):  # pragma: no cover
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
            message = process_user_message(text, user)

            if user != "U031T0UHLH1":
                channel = event_message.get("channel")
                client.chat_postMessage(
                    blocks=[{"type": "section", "text": {"type": "mrkdwn", "text": message}}], channel=channel
                )
                return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_200_OK)
