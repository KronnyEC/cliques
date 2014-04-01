from django.core.mail import send_mail
from django.db import models
from django import forms
import random
from django.conf import settings
from urllib import urlencode


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
        print("qs: {}".format(query_string))

        send_mail(subject="SlasherTraxx Invite",
                  message="Link: http://slashertraxx.com/accounts/signup/?{}"
                          .format(query_string),
                  from_email="invite@slashertraxx.com",
                  recipient_list=[self.cleaned_data['email']])