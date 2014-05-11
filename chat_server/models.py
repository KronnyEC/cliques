from django.db import models
from website.models import UserProfile


# Create your models here.
class ChatUser(models.Model):
    user = models.ForeignKey(UserProfile)
    token = models.CharField(max_length=255)
    connected_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "{0}: {1}, connected: {2}".format(self.user.username,
                                                 self.token,
                                                 self.connected_at)

    def __repr__(self):
        return "<{0}, {1}>".format(ChatUser, self.__unicode__())


class ChatMessage(models.Model):
    user = models.ForeignKey(UserProfile)
    message = models.TextField()
    sent = models.DateTimeField(auto_now_add=True, db_index=True)

    def __unicode__(self):
        return "{0}: {1}".format(self.user.username,
                                                 self.message)

    def __repr__(self):
        return "<{0}, {1}>".format(ChatMessage, self.__unicode__())
