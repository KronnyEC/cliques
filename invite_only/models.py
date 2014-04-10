from django.core.mail import send_mail
from django.db import models
from django import forms
import random
from django.conf import settings
from urllib import urlencode
import logging

if settings.ENV == 'appengine':
    from google.appengine.api import mail

logger = logging.getLogger(__name__)


def random_code():
    return '%08x' % random.randrange(16**8)


class InviteCode(models.Model):
    invited_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    code = models.CharField(max_length=32, default=random_code, unique=True)
    used = models.BooleanField(default=False)
    #TODO(pcsforeducation) Add site FK


class InviteForm(forms.Form):
    email = forms.EmailField()
    name = forms.CharField()

    def save(self, user, commit=True):
        self.invite = InviteCode(invited_by=user)
        self.invite.save()
        self.send_code(self.invite.code)

    def send_code(self, code):
        query = {
            'email': self.cleaned_data['email'],
            'invite_code': code
        }
        query_string = urlencode(query)
        subject = "SlasherTraxx Invite"
        body = "Link: http://www.slashertraxx.com/accounts/signup/?{}".format(
            query_string)
        from_email = "josh@slashertraxx.com"
        recipient_list = [self.cleaned_data['email']]
        logging.info("Sending invite mail from {} to {}, subject: {}, "
                     "messages: {}. MAIL_PROVIDER: {}".format(
                         from_email, recipient_list, subject, body,
                         settings.MAIL_PROVIDER))
        if settings.MAIL_PROVIDER == "APPENGINE":
            # mail.send_mail(from_email, recipient_list[0], subject, message)
            message = mail.EmailMessage(
                sender="SlasherTraxx Invite <josh@slashertraxx.com>",
                subject="SlasherTraxx Invite")

            message.to = self.cleaned_data['email']
            message.body = body
            message.send()
        else:
            send_mail(subject, body, from_email, recipient_list)


