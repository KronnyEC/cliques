import json
import logging
from datetime import timedelta, datetime

from google.appengine.api import channel
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework import generics
from rest_framework import renderers
from rest_framework import status

from chat_server.serializers import ChatMessageSerializer, ChatSessionSerializer
from chat_server.models import ChatMessage, ChatSession
from rest_framework.decorators import link, action
from rest_framework.response import Response

logger = logging.getLogger(__name__)


class ChatSessionList(generics.ListCreateAPIView):
    model = ChatSession
    serializer_class = ChatSessionSerializer

    paginate_by = 50
    paginate_by_param = 'sessions'
    max_paginate_by = 1000

    def pre_save(self, obj):
        obj.user = self.request.user
        obj.session_key = channel.create_channel(obj.user.username, 24 * 60)
        logger.info("Presave, Created token {} for {}".format(
            obj.session_key, obj.user.username))
        super(ChatSessionList, self).pre_save(obj)

    @link()
    def check_in(self, session_key):
        if not session_key:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            obj = ChatSession.objects.get(session_key=session_key)
        except ChatSession.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        obj.save()
        return Response(status=status.HTTP_202_ACCEPTED)


class ChatMessageList(generics.ListCreateAPIView):
    model = ChatMessage
    serializer_class = ChatMessageSerializer
    queryset = ChatMessage.objects.all()

    paginate_by = 25
    paginate_by_param = 'messages'
    max_paginate_by = 1000

    def post_save(self, obj, created=False):
        # Update the session so it doesn't get dropped
        obj.session.save()
        if created:
            # Send out the message to everyone. Support for editing messages
            # may come later. Maybe not.
            j = json.dumps({
                'type': 'chat',
                'data': obj.to_json()
            }, cls=DjangoJSONEncoder)
            five_mins_ago = datetime.now() - timedelta(minutes=5)
            for session in ChatSession.objects.filter(ended__isnull=True).filter(last_update__gt=five_mins_ago):
                channel.send_message(session.session_key, j)
