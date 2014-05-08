from django.db import models
from website.models import UserProfile


NOTIFICATION_TYPES = (('comment', 'comment'), )
NOTIFICATION_LEVELS = (('debug', 'Debug'), ('info', 'Info'),
                       ('success', 'Success'), ('warning', 'Warning'),
                       ('error', 'Error'))


class Notification(models.Model):
    text = models.TextField()
    user = models.ForeignKey(UserProfile)
    type = models.CharField(max_length=64, choices=NOTIFICATION_TYPES)
    level = models.CharField(max_length=16, choices=NOTIFICATION_LEVELS,
                             default='info')
    link = models.URLField()
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __unicode__(self):
        return "{}: {}".format(self.user.username, self.text)

    def __repr__(self):
        return self.__unicode__()
