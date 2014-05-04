from notify.models import Notification
from rest_framework import serializers


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id', 'text', 'user', 'type', 'level', 'link',
                  'created_at')