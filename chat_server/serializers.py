from rest_framework import serializers
from chat_server.models import ChatMessage


class ChatMessageSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(source='user', read_only=True)

    class Meta:
        model = ChatMessage
        fields = ('message', 'sent', 'user')
