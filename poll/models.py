from django.db import models
from django import forms
from website.utils import detect_content_type
from website.models import UserProfile

FREQUENCY_CHOICES = (('daily', 'daily'), ('once', 'once'))


class Poll(models.Model):
    title = models.CharField(max_length=255)
    stub = models.CharField(max_length=32)
    bot_name = models.CharField(max_length=32)
    # In hours
    frequency = models.IntegerField(default=24)
    # In hours, when old submissions that haven't won will be removed
    submission_removal = models.IntegerField(default=7*24)


class Submission(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    submitted = models.DateTimeField(auto_now_add=True)
    votes = models.ManyToManyField(UserProfile, through='Vote')
    poll = models.ForeignKey(Poll, related_name='poll_submissions')
    user = models.ForeignKey(UserProfile, related_name='user_submissions')

    def save(self, *args, **kwargs):
        if self.id is None:
            new = True
        else:
            new = False

        super(Submission, self).save(*args, **kwargs)
        # Check if text field is
        self.type = detect_content_type(self.url)
        if not new:
            return


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['title', 'url']


class Vote(models.Model):
    submission = models.ForeignKey(Submission, related_name='submission_votes')
    user = models.ForeignKey(UserProfile, related_name='user_votes')
    day = models.DateField(auto_now_add=True)

    class Meta:
        # One vote per user per day.
        unique_together = (('submission', 'day'))

    def __unicode__(self):
        return "{} voted on {} on {}".format(self.user.username,
                                             self.submission.title,
                                             self.day)