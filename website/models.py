import logging
import urlparse

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django import forms

from website.content_types import YouTube
from website.utils import detect_content_type


if settings.ENV == 'appengine':
    from google.appengine.api import mail

logger = logging.getLogger(__name__)

POST_TYPES = (('link', 'link'), ('image', 'image'),
              ('video', 'video'), ('youtube', 'youtube'), ('text', 'text'))

EMAIL_PREFERENCES = (('no', 'None'), ('posts', 'New Posts Only'),
                     ('all', 'Posts and Comments'))

CATEGORY_COLORS = (('red', 'Red'), ('blue', 'Blue'), ('purple', 'Purple'),
                   ('orange', 'Orange'), ('green', 'Green'))


class UserProfile(AbstractUser):
    profile_pic = models.ImageField(upload_to='cliques-profile', blank=True,
                                    null=True, default=None)
    email_settings = models.CharField(max_length=64, choices=EMAIL_PREFERENCES,
                                      default='posts')
    poll_votes = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)


class Category(models.Model):
    created_by = models.ForeignKey(UserProfile)
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=64, choices=CATEGORY_COLORS)

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return "<{0}, {1}>".format(Category, self.__unicode__())


class Post(models.Model):
    submitted = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(UserProfile)
    title = models.CharField(max_length=255)
    url = models.URLField(blank=True, null=True)
    type = models.CharField(max_length=64, choices=POST_TYPES, default="link")
    thumbnail_height = models.IntegerField(default=0)
    thumbnail_width = models.IntegerField(default=0)
    thumbnail = models.ImageField(blank=True,
                                  default=None,
                                  null=True,
                                  upload_to='media'
    )
    category = models.ForeignKey(Category)

    def save(self, *args, **kwargs):
        if self.id is None:
            new = True
        else:
            new = False
        self.type = detect_content_type(self.url)

        super(Post, self).save(*args, **kwargs)

        logger.info('type {} is {}'.format(self.title, self.type))
        if new:
            self._new_post_email()

    def _new_post_email(self):
        # TODO(pcsforeducation) Make async
        if self.type in ['youtube', 'video']:
            post_type = 'video'
        elif self.type == 'text':
            post_type = 'text post'
        elif self.type in ['imgur', 'image']:
            post_type = 'image'
        else:
            logger.warning('Post {} was of type none'.format(self.title))
            post_type = 'none'

        # Send email to everyone posts or all for new posts
        users_to_email = UserProfile.objects.filter(
            email_settings__in=['all', 'posts']) \
            .exclude(email=u'').values_list('email', flat=True)

        if not users_to_email:
            logger.info("No users to email for post {}. Whomp Whomp.".format(
                self.id))

        subject = '[slashertraxx] {} - {}'.format(self.title,
                                                  self.user.username)

        message = '''
        {username} posted a new {post_type}.

        {title}

        http://slashertraxx.com/post/{id}/

        To unsubscribe, go to http://slashertraxx.com/users/
        '''.format(**{
            'username': self.user.username,
            'post_type': post_type,
            'id': self.id,
            'title': self.title,
            'url': self.url or ''
        })

        logger.info("Sending email to {}, subject {}, message {}".format(
            users_to_email, subject, message))
        send(users_to_email, subject, message)

    def youtube_video_id(self):
        youtube = YouTube()
        return youtube.youtube_video_id(self.url)

    def domain(self):
        try:
            url = urlparse.urlparse(self.url)
        except Exception:
            return "unknown"
        return url.netloc

    def __unicode__(self):
        return "{0}: {1}".format(self.type, self.title)

    def __repr__(self):
        return "<{0}, {1}>".format(Post, self.__unicode__())

    class Meta:
        ordering = ["-submitted"]


class Comment(models.Model):
    user = models.ForeignKey(UserProfile)
    text = models.TextField()
    submitted = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post)

    def __unicode__(self):
        return "{0}: {1}".format(self.user, self.text)

    def __repr__(self):
        return "<{0}, {1}>".format(Post, self.__unicode__())


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__()
        self.fields['title'].label = "Title (*)"
        self.fields['url'].label = "Link"
        self.fields['category'].label = "Category"

    def save(self, commit=True):
        instance = super(PostForm, self).save(commit=False)

        instance.save(commit)
        return instance

    class Meta:
        model = Post
        fields = ['title', 'url', 'category']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class ProfileUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__()

    class Meta:
        model = UserProfile
        fields = ['email', 'email_settings']


# class ProfileRegistrationForm(RegistrationForm):
# is_human = forms.ChoiceField(label = "Are you human?:")


def send(recipient_list, subject, body):
    from_email = "josh@slashertraxx.com"
    logging.info("Sending invite mail from {} to {}, subject: {}, "
                 "messages: {}. MAIL_PROVIDER: {}".format(
        from_email, recipient_list, subject, body,
        settings.MAIL_PROVIDER))
    if settings.MAIL_PROVIDER == "APPENGINE":
        # mail.send_mail(from_email, recipient_list[0], subject, message)
        message = mail.EmailMessage(
            sender="SlasherTraxx <josh@slashertraxx.com>",
            subject=subject)

        message.to = recipient_list
        message.body = body
        message.send()
    else:
        send_mail(subject, body, from_email, recipient_list)
