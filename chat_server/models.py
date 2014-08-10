import random
from django.db import models
from django.conf import settings


def random_key(length=64):
    return ''.join(random.choice('0123456789ABCDEF') for i in range(length))


class ChatMessage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    message = models.TextField()
    sent = models.DateTimeField(auto_now_add=True, db_index=True)

    def __unicode__(self):
        return "{0}: {1}".format(self.session, self.message)

    def __repr__(self):
        return "<{0}, {1}>".format(ChatMessage, self.__unicode__())

    def to_json(self):
        return {
            'user': self.user.id,
            'username': self.user.username,
            'message': self.message,
            'sent': self.sent
        }

    class Meta:
        ordering = ['-sent']
