import logging

from rest_framework import generics

from .serializers import PushSessionSerializer
from .models import PushSession

logger = logging.getLogger(__name__)


class PushSessionList(generics.CreateAPIView):
    model = PushSession
    serializer_class = PushSessionSerializer

    def pre_save(self, obj):
        # Disable existing sessions for this user
        obj.user = self.request.user
        super(PushSessionList, self).pre_save(obj)
