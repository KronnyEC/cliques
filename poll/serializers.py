from rest_framework import serializers
from poll.models import Poll, Submission, Vote


class SubmissionSerializer(serializers.ModelSerializer):
    # poll = serializers.WritableField(source='poll', required=False)
    class Meta:
        model = Submission
        fields = ('title', 'url', 'submitted', 'poll', 'id')


class PollSerializer(serializers.ModelSerializer):

    class Meta:
        model = Poll
        fields = ('title', 'stub', 'bot_name', 'category',
                  'frequency', 'submission_removal', 'winning_text',
                  'poll_submissions', 'id')

        depth = 1


class VoteSerializer(serializers.ModelSerializer):
    day = serializers.Field(source='day')

    class Meta:
        model = Vote
        fields = ('submission', 'user', 'day', 'id')
