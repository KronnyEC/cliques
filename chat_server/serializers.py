from rest_framework import serializers
from chat_server.models import ChatMessage, ChatSession


class ChatMessageSerializer(serializers.ModelSerializer):
    session = serializers.PrimaryKeyRelatedField()
    username = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = ChatMessage
        fields = ('session', 'message', 'sent', 'username')
        depth = 1


class ChatSessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChatSession
        fields = ('id', 'started', 'last_update', 'ended', 'session_key')
        depth = 1