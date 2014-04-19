import json
import urlparse
import logging
import sys
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse

import urllib3
from django.conf import settings

logger = logging.getLogger(__name__)


class ContentType(object):
    def __init__(self, url, content_type):
        self.url = url
        self.content_type = content_type

    def detect(self, url, content_type):
        pass

    def render(self):
        return None


class Video(ContentType):
    def detect(self, url, content_type):
        return 'video'


class Image(ContentType):
    def detect(self, url, content_type):
        return 'image'


class YouTube(Video):
    def detect(self, url, content_type):
        url_data = urlparse.urlparse(url)
        query = urlparse.parse_qs(url_data.query)
        if len(query.get("v", [])) > 0:
            # return query["v"][0]
            return 'youtube'

    def youtube_video_id(self, url):
        url_data = urlparse.urlparse(url)
        query = urlparse.parse_qs(url_data.query)
        if len(query.get("v", [])) > 0:
            return query["v"][0]


class Imgur(ContentType):
    def detect(self, url, content_type):
        url_data = urlparse.urlparse(url)
        if url_data.netloc() == 'imgur.com':
            return 'imgur'


content_types = {
    'image': [
        'Imgur',
        'Image'
    ],
    'video': [
        'Youtube',
        'Video'
    ],
    'link': [
        'Link'
    ]
}


def get_class_from_string(class_name):
    return getattr(sys.modules[__name__], class_name)


def detect_content_type(url=None):
    # Default
    if url is None:
        return 'text'

    # Get mime type of remote url
    try:
        http = urllib3.PoolManager()
        response = http.request('HEAD', url)
        content_type = response.headers.get('content-type')
    except Exception:
        return None

    # Find list of content detectors based on mime
    if content_type in settings.MIME_IMAGES:
        key = 'image'
    elif content_type in settings.MIME_VIDEO or 'youtube.com' in url:
        key = 'video'
    else:
        key = 'link'

    # Go through content detectors in order, returning if any matches
    for content_type in content_types[key]:
        cls = get_class_from_string(content_type)()
        detected_type = cls.detect(url, content_type)
        if detected_type:
            return detected_type


def render_to_json(request, data):
    # msgs = {}
    # messages_list = messages.get_messages(request)
    # count = 0
    # for message in messages_list:
    #     msgs[count] = {'message': message.message, 'level': message.level}
    #     count += 1
    # data['messages'] = msgs
    return HttpResponse(
        json.dumps(data, ensure_ascii=False, cls=DjangoJSONEncoder),
        content_type=request.is_ajax() and "application/json" or "text/html"
    )
