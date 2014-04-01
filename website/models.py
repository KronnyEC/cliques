from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db import models
from django import forms
from django.conf import settings
import os
# import requests
import urllib3
from django.core.files import File
# from PIL import Image
# from registration.forms import RegistrationForm


POST_TYPES = (('link', 'link'), ('text', 'text'), ('image', 'image'),
              ('video', 'video'), ('youtube', 'youtube'))


class UserProfile(AbstractUser):
    profile_pic = models.ImageField(upload_to='traxx-profile')


class Post(models.Model):
    submitted = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    user = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    text = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    type = models.CharField(max_length=64, choices=POST_TYPES)
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
            validate(self.text)
        except ValidationError:
            # Not a URL, just save as text
            self.type = 'text'
            return False
        return True

    def detect_content_type(self):
        # Get mime type of remote URL
        http = urllib3.PoolManager()
        response = http.request('HEAD', self.text)
        content_type = response.headers.get('content-type')
        # print 'content type', content_type
        if content_type in settings.MIME_IMAGES:
            self.set_image()
            return 'image'
        elif content_type in settings.MIME_VIDEO or 'youtube.com' in self.text:
            self.set_video()
            return 'video'
        else:
            self.set_link()
            return 'link'

    def set_image(self):
        self.type = 'image'
        self.url = self.text
        self.text = None

    def set_video(self):
        # print 'found video'
        self.url = self.text
        # Attempt to find video source. If YouTube, deal with it
        #TODO(pcsforeducation) use requests
        # url_data = urlparse.urlparse(self.url)
        # query = urlparse.parse_qs(url_data.query)
        url_data = None
        query = None
        video = query["v"][0]
        if video is not None:
            self.text = video
            self.type = 'youtube'
        else:
            self.text = None
            self.type = 'video'

    def set_link(self):
        self.type = 'link'
        self.url = self.text
        self.text = None

    def save(self, *args, **kwargs):
        self.text = self.text.strip()
        # Check if text field is
        # print 'detecting link'
        # if self.detect_link():
            # print 'detected'
            # print self.detect_content_type()
            # print 'detect'
        # print 'type detected'
        # print 'text', self.text
        # print 'url', self.url
        # print 'type', self.type
        super(Post, self).save(*args, **kwargs)

    # Do asyncronously later.
    def make_thumbnail(self):
        if self.type == 'image':
            # Download the image, make a thumbnail, and upload to cloudfiles.
            tmp_file = self._download_url(self.url)
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
        self.fields['text'].label = "Text/Link"

    def save(self, commit=True):
        instance = super(PostForm, self).save(commit=False)
        instance.save(commit)
        return instance

    class Meta:
        model = Post
        fields = ['title', 'text']


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__()

    class Meta:
        model = Comment
        fields = ['text']


# class ProfileRegistrationForm(RegistrationForm):
#     is_human = forms.ChoiceField(label = "Are you human?:")