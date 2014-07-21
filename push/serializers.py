from rest_framework import serializers
from .models import PushSession


class PushSessionSerializer(serializers.ModelSerializer):
    started = serializers.CharField(max_length=255, read_only=True)
    last_update = serializers.CharField(max_length=255, read_only=True)
    ended = serializers.CharField(max_length=255, read_only=True)
    session_key = serializers.CharField(max_length=255, read_only=True)
    user = serializers.PrimaryKeyRelatedField(source='user', read_only=True)

    class Meta:
        model = PushSession
        fields = ('started', 'last_update', 'ended', 'session_key',
                  'user')
        depth = 1