from rest_framework import serializers
from chat_server.models import ChatMessage, ChatSession


class ChatMessageSerializer(serializers.ModelSerializer):
    session = serializers.PrimaryKeyRelatedField()

    class Meta:
        model = ChatMessage
        fields = ('session', 'message', 'sent')
        depth = 1


class ChatSessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChatSession
        fields = ('id', 'started', 'last_update', 'ended', 'session_key')
        depth = 1