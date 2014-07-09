from rest_framework import generics, permissions

from poll.models import Poll, Submission, Vote
from poll.serializers import PollSerializer, SubmissionSerializer, \
    VoteSerializer


class PollDetail(generics.RetrieveAPIView):
    lookup_field = 'stub'
    model = Poll
    serializer_class = PollSerializer
    permission_classes = [
        permissions.AllowAny
    ]
    depth = 1


class PollList(generics.ListCreateAPIView):
    model = Poll
    serializer_class = PollSerializer
    permission_classes = [
        permissions.AllowAny
    ]


class VoteList(generics.ListCreateAPIView):
    model = Vote
    serializer_class = VoteSerializer
    permission_classes = [
        permissions.AllowAny
    ]

    def pre_save(self, obj):
        obj.user = self.request.user

    def get_queryset(self):
        return Vote.objects.filter(user=self.request.user)


class VoteDetail(generics.RetrieveDestroyAPIView):
    model = Vote
    serializer_class = VoteSerializer
    permission_classes = [
        permissions.AllowAny
    ]

    def pre_save(self, obj):
        obj.user = self.request.user


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

    def pre_save(self, obj):
        obj.user = self.request.user