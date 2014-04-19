from django.db import models
from website.utils import detect_content_type
from website.models import UserProfile


class Submission(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    submitted = models.DateTimeField(auto_now_add=True)
    votes = models.ManyToManyField(UserProfile, through='Vote')

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


class Vote(models.Model):
    submission = models.ForeignKey('Submission')
    user = models.ForeignKey('UserProfile')
    day = models.DateField(auto_now_add=True)

    class Meta:
        # One vote per submission per user per day.
        unique_together = (('submission', 'user', 'day'))