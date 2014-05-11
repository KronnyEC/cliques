from rest_framework import serializers
from poll.models import Poll, Submission


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ('title', 'url', 'submitted', 'poll')


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ('title', 'stub', 'bot_name', 'category',
                  'frequency', 'submission_removal', 'winning_text')
