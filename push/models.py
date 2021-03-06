import datetime
import json
import logging
import random

from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.conf import settings
from google.appengine.api import channel

logger = logging.getLogger(__name__)


def random_key(length=64):
    return ''.join(random.choice('0123456789ABCDEF') for i in range(length))


class PushSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    started = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True, db_index=True)
    session_key = models.CharField(max_length=255, default=None,
                                   db_index=True, unique=True)
    ended = models.DateTimeField(blank=True, null=True, default=None)

    def send_message(self, message_type, message):
        j = json.dumps({
            'type': message_type,
            'data': message
        }, cls=DjangoJSONEncoder)
        channel.send_message(self.session_key, j)

    def save(self, *args, **kwargs):
        self.session_key = channel.create_channel(random_key(), 24 * 60)
        super(PushSession, self).save(*args, **kwargs)

    def __unicode__(self):
        return "{0}: {1}, connected: {2}".format(self.user,
                                                 self.session_key,
                                                 self.started)

    def __repr__(self):
        return "<{0}, {1}>".format(PushSession, self.__unicode__())


def get_all_connected(user=None):
    timeout = getattr(settings, 'PUSH_SESSION_TIMEOUT', 300)
    timeout_dt = datetime.datetime.now() - datetime.timedelta(seconds=timeout)
    sessions = PushSession.objects.filter(ended__isnull=True).filter(
        last_update__gt=timeout_dt)
    if user:
        sessions = sessions.filter(user=user)
    logger.debug("Conencted users: {}".format(sessions))
    return sessions


def send_all(message_type, message, user=None):
    sessions = get_all_connected(user)
    logger.info("Sending {}:{} to {}".format(message_type, message, sessions))
    for session in sessions:
        session.send_message(message_type, message)
