import logging

from rest_framework import generics

from .models import ChatMessage
from .serializers import ChatMessageSerializer
from push.models import send_all

logger = logging.getLogger(__name__)


class ChatMessageList(generics.ListCreateAPIView):
    model = ChatMessage
    serializer_class = ChatMessageSerializer
    queryset = ChatMessage.objects.all()

    paginate_by = 25
    paginate_by_param = 'messages'
    max_paginate_by = 1000

    def pre_save(self, obj):
        obj.user = self.request.user
        super(ChatMessageList, self).pre_save(obj)

    def post_save(self, obj, created=False):
        if created:
            data = obj.to_json()
            logger.info("sending chat to all: {}", data)
            send_all('chat', data)
        else:
            logger.warning("not created message?")
