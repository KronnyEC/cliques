"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import datetime

from django.test import TestCase

from website.models import Post, Category, UserProfile


default_post = {
    'submitted': datetime.datetime(2014, 1, 1),
    'edited': datetime.datetime(2014, 1, 1),
    'title': 'Fake title!',
    'url': 'http://google.com/?q=clique',
    'type': 'link',
    'thumbnail_height': 0,
    'thumbnail_width': 0,
    'thumbnail': 'http://example.com/thumbnail.gif'
}


default_category = {
    'name': 'Category',
    'color': 'burntsienna'
}


default_user_profile = {
    'profile_pic': None,
    'email_settings': 'all',
    'poll_votes': 1,
    'password': 'test_password',
    'username': 'the_user',
    'last_login': datetime.datetime(2014, 1, 3),
    'is_superuser': False,
    'first_name': 'Flynn',
    'last_name': 'Tron',
    'email': 'flynn@flynncorp.net',
    'is_staff': False,
    'is_active': True,
    'date_joined': datetime.datetime(2014, 1, 1),
}


default_comment = {
    'user': 1,
    'text': 'This is a comment.\nThis is line two.',
    'submitted': datetime.datetime(2014, 1, 2),
    'edited': datetime.datetime(2014, 1, 3),
    'post': 1
}


class WebsiteAPITest(TestCase):
    def setUp(self):
        # super(WebsiteAPITest, self).__init__()
        self.user = self._create_test_user()
        self.category = self._create_test_category()
        self.post = self._create_test_post()

    def _create_test_object(self, cls, defaults, kwargs):
        for field in cls._meta.fields:
            if field.name != 'id' and field.name not in kwargs:
                kwargs[field.name] = defaults[field.name]
        print 'test kwrags', kwargs, cls
        a = cls(**kwargs)
        print 'test ob', a
        return a

    def _create_test_post(self, **kwargs):
        if 'user' not in kwargs:
            kwargs['user'] = self.user
        if 'category' not in kwargs:
            kwargs['category'] = self.category
        return self._create_test_object(Post, default_post, kwargs)

    def _create_test_user(self, **kwargs):
        print "CREATE_TEST_USER"
        a = self._create_test_object(
            UserProfile, default_user_profile, kwargs)
        print "returning", a
        return a

    def _create_test_category(self, **kwargs):
        print "CATEGORY", kwargs, self.user
        if 'created_by' not in kwargs:
            kwargs['created_by'] = self.user
        print "CATEGORY", kwargs
        return self._create_test_object(Category, default_category, kwargs)

    def test_simple_post_list(self):
        post_list = None
        self.assertEqual([self.post], post_list)

    def test_multiple_post_list(self):
        post2 = self._create_test_post()
        post_list = None
        self.assertEqual([post2, self.post], post_list)

    def test_create_post(self):
        # post_data = default_post
        pass
