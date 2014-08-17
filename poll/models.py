from django.core.exceptions import ValidationError
from django.db import models
from django import forms
from website.utils import detect_content_type
from website.models import UserProfile, Category

FREQUENCY_CHOICES = (('daily', 'daily'), ('once', 'once'))


class Poll(models.Model):
    title = models.CharField(max_length=255)
    stub = models.CharField(max_length=32)
    bot_name = models.CharField(max_length=32)
    category = models.ForeignKey(Category)
    # In hours
    frequency = models.IntegerField(default=24)
    # In hours, when old submissions that haven't won will be removed
    submission_removal = models.IntegerField(default=7 * 24)
    winning_text = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return self.title


class Submission(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    submitted = models.DateTimeField(auto_now_add=True)
    votes = models.ManyToManyField(UserProfile, through='Vote')
    poll = models.ForeignKey(Poll, related_name='poll_submissions')
    user = models.ForeignKey(UserProfile, related_name='user_submissions')
    # The text that will be show below a winning submission

    def save(self, *args, **kwargs):
        if Submission.objects.filter(user=self.user).count() > 4:
            raise ValidationError('More than 5 submissions.')
        super(Submission, self).save(*args, **kwargs)
        # Check if text field is
        self.type = detect_content_type(self.url)

    def __unicode__(self):
        return "{}: {}".format(self.user, self.title)


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['title', 'url']


class Vote(models.Model):
    submission = models.ForeignKey(Submission, related_name='submission_votes')
    user = models.ForeignKey(UserProfile, related_name='user_votes')
    day = models.DateField(auto_now_add=True)

    def validate_unique(self, exclude=None):
        super(Vote, self).validate_unique(exclude)
        if Vote.objects.filter(user=self.user).count() > 2:
            raise ValidationError('More than 3 votes.')

    def __unicode__(self):
        return "{} voted on {} on {}".format(self.user.username,
                                             self.submission.title,
                                             self.day)