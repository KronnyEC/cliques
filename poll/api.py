from rest_framework import generics, permissions

from poll.models import Poll, Submission
from poll.serializers import PollSerializer, SubmissionSerializer


class PollDetail(generics.RetrieveAPIView):
    model = Poll
    serializer_class = PollSerializer
    permission_classes = [
        permissions.AllowAny
    ]


class PollList(generics.ListCreateAPIView):
    model = Poll
    serializer_class = PollSerializer
    permission_classes = [
        permissions.AllowAny
    ]


class SubmissionDetail(generics.RetrieveAPIView):
    model = Submission
    serializer_class = SubmissionSerializer
    permission_classes = [
        permissions.AllowAny
    ]


class SubmissionList(generics.ListCreateAPIView):
    model = Submission
    serializer_class = SubmissionSerializer
    permission_classes = [
        permissions.AllowAny
    ]
