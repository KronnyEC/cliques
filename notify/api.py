from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from notify.models import Notification
from notify.serializers import NotificationSerializer
from rest_framework.response import Response
from rest_framework.views import APIView


class NotificationList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    model = Notification
    paginate_by = 5
    paginate_by_param = 'num_notifications'
    max_paginate_by = 20

    def get(self, request, format=None):
        if not self.request.user.is_authenticated():
            return HttpResponseForbidden()
        notifications = self.get_queryset()
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

    def delete(self, request, format=None):
        if not self.request.user.is_authenticated():
            return HttpResponseForbidden()
        notifications = self.get_queryset()
        print notifications
        notifications.delete()
        return Response('ok')

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        return Notification.objects.filter(user=user)