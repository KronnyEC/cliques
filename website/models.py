import logging
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db import models
from django import forms
from django.conf import settings
import os
import urlparse
import urllib3
from django.core.files import File
if settings.ENV == 'appengine':
    from google.appengine.api import mail

logger = logging.getLogger(__name__)

POST_TYPES = (('link', 'link'), ('image', 'image'),
              ('video', 'video'), ('youtube', 'youtube'), ('text', 'text'))

EMAIL_PREFERENCES = (('no', 'None'), ('posts', 'New Posts Only'),
                     ('all', 'Posts and Comments'))


class UserProfile(AbstractUser):
    profile_pic = models.ImageField(upload_to='traxx-profile', blank=True,
                                    null=True, default=None)
    email_settings = models.CharField(max_length=64, choices=EMAIL_PREFERENCES,
                                      default='no')


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

    def detect_link(self):
        validate = URLValidator()
        try:
            validate(self.url)
        except ValidationError:
            # Not a URL, just save as text
            self.type = 'text'
            return False
        return True

    def detect_content_type(self):
        # Get mime type of remote URL
        logger.info(self.url)
        if not self.url:
            self.type = 'text'
            return 'text'
        if self.url is not None:
            try:
                http = urllib3.PoolManager()
                response = http.request('HEAD', self.url)
                content_type = response.headers.get('content-type')
            except Exception:
                content_type = None
        else:
            content_type = None

        # print 'content type', content_type
        if content_type in settings.MIME_IMAGES:
            self.set_image()
            return 'image'
        elif content_type in settings.MIME_VIDEO or 'youtube.com' in self.url:
            self.set_video()
            return 'video'
        else:
            self.set_link()
            return 'link'

    def set_image(self):
        self.type = 'image'
        # self.url = None

    def set_video(self):
        # print 'found video'
        # Attempt to find video source. If YouTube, deal with it
        #TODO(pcsforeducation) use requests
        video = self.youtube_video_id()
        if video is not None:
            self.type = 'youtube'
        else:
            self.type = 'video'

    def set_link(self):
        self.type = 'link'

    def save(self, *args, **kwargs):
        # Check if text field is
        self.detect_content_type()
        super(Post, self).save(*args, **kwargs)
        # Send email to everyone posts or all
        users_to_email = UserProfile.objects.filter(
            email_settings__in=['all', 'posts'])
        users_to_email = users_to_email.values_list('email', flat=True)

        if not users_to_email:
            logger.info("No users to email for post {}. Whomp Whomp.".format(
                self.id))

        subject = '[slashertraxx] {} - {}'.format(self.title, self.user.username)

        post_type = self.type
        if post_type == 'youtube':
            post_type = 'video'
        elif post_type == 'text':
            post_type = 'text post'

        message = '{} posted a new {}. <a href="http://slashertraxx.com/posts/{}/">Click here to view post.' \
                  '</a>'.format(self.user.username, post_type, self.id)

        logger.info("Sending email to {}, subject {}, message {}".format(
            users_to_email, subject, message))
        send(users_to_email, subject, message)

    def youtube_video_id(self):
        url_data = urlparse.urlparse(self.url)
        query = urlparse.parse_qs(url_data.query)
        if len(query.get("v", [])) > 0:
            return query["v"][0]
        else:
            return None

    # Do asyncronously later.
    def make_thumbnail(self):
        if self.type == 'image':
            # Download the image, make a thumbnail, and upload to cloudfiles.
            tmp_file = self._download_url(self.text)
            thumbnail = self._make_thumbnail(tmp_file)
            self.thumbnail = File(open(thumbnail))

    def _download_url(self, url):
        local_filename = url.split('/')[-1]
        # print "saving to: ", local_filename
        # NOTE the stream=True parameter
        http = urllib3.PoolManager()
        r = http.request('GET', self.text)
        with open(os.path.join(settings.TMP_DIR, local_filename), 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush()
        # print "saved"
        return os.path.join(settings.TMP_DIR, local_filename)

    def _make_thumbnail(self, filename):
        # print 'API', settings.CUMULUS['API_KEY']
        outfilename = os.path.splitext(filename)[0] + ".thumbnail"
        outfile = os.path.join(settings.THUMBNAIL_DIR, outfilename)
        # print "saving thumbnail: ", outfile
        try:
            im = Image.open(filename)
            im.thumbnail(settings.THUMBNAIL_MAX_SIZE, Image.ANTIALIAS)
            im.save(outfile, "JPEG")
        except IOError as e:
            pass
            # print e
            # print "cannot create thumbnail for '%s'" % filename
        # print "saved"
        return outfile

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


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__()
        self.fields['title'].label = "Title (*)"
        self.fields['url'].label = "Link"

    def save(self, commit=True):
        instance = super(PostForm, self).save(commit=False)
        instance.save(commit)
        return instance

    class Meta:
        model = Post
        fields = ['title', 'url', 'user']


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__()

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
#     is_human = forms.ChoiceField(label = "Are you human?:")


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


