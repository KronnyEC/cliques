import json
import random
from django.db import models
from website.models import UserProfile


def random_key(length=64):
    return ''.join(random.choice('0123456789ABCDEF') for i in range(length))


class ChatSession(models.Model):
    user = models.ForeignKey(UserProfile)
    started = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True, db_index=True)
    session_key = models.CharField(max_length=255, default=random_key,
                                   db_index=True, unique=True)
    ended = models.DateTimeField(blank=True, null=True, default=None)

    def __unicode__(self):
        return "{0}: {1}, connected: {2}".format(self.user.username,
                                                 self.session_key,
                                                 self.started)

    def __repr__(self):
        return "<{0}, {1}>".format(ChatSession, self.__unicode__())


class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession)
    message = models.TextField()
    sent = models.DateTimeField(auto_now_add=True, db_index=True)

    def __unicode__(self):
        return "{0}: {1}".format(self.user.username,
                                                 self.message)

    def __repr__(self):
        return "<{0}, {1}>".format(ChatMessage, self.__unicode__())

    def to_json(self):
        return json.dumps({
            'user': self.session.user.username,
            'message': self.message,
            'sent': self.sent
        })
