from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.generic import DetailView
from website.views import PostsListView, PostFormView, CommentFormView, \
    PostDetailView, ProfileDetailView, ProfileEditView
from website.models import Post, UserProfile
from django.contrib import admin
from invite_only.models import InviteCode
from invite_only.views import InviteCodeView
# from registration.views import RegistrationView
from website.api import PostList, PostDetail, PostCommentList
from website.api import CommentList, CommentDetail
from website.api import UserPostList, UserDetail


admin.autodiscover()

post_detail = login_required(PostDetailView.as_view(model=Post))
post_list = login_required(PostsListView.as_view(model=Post))
post_form = login_required(PostFormView.as_view())
profile_detail = login_required(ProfileDetailView.as_view(model=UserProfile))
profile_update = login_required(ProfileEditView.as_view())
invite_form = login_required(InviteCodeView.as_view())
comment_form = login_required(CommentFormView.as_view())

v1_post_urls = patterns('',
    url(r'^posts/$', PostList.as_view(), name='post-list'),
    url(r'^posts/(?P<pk>\d+)/$', PostDetail.as_view(), name='post-detail'),
    url(r'^posts/(?P<pk>\d+)/comments/$', PostCommentList.as_view(),
        name='post-comment-list')
)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'traxx.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'accounts/register/$',
    #     RegistrationView.as_view(form_class=ProfileRegistrationForm),
    #     name='registration_register'),
    # (r'^accounts/logout/$', 'django.contrib.auth.views.logout',
    #                       {'next_page': '/'}),
    url(r'^accounts/', include('allauth.urls')),
    # url(r'^accounts/', include('invite_only.urls')),
    url(r'^auth/', include('django.contrib.auth.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', post_list, name='post_list', ),
    url(r'^post/$', require_POST(post_form),
        name='post_form_view_url'),
    url(r'^post/(?P<pk>[a-f\d]+)/$', post_detail, name='post_detail'),
    url(r'^post/(?P<pk>[a-f\d]+)/comment/$',
        require_POST(comment_form),
        name='post_form_view_url'),
    url(r'^invite/$', invite_form, name='invite_form'),
    url(r'^users/$', 'website.views.user_redirect'),
    url(r'^users/(?P<slug>\w+)/$', profile_update, name='profile_detail'),

    # API
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url('^api/v1/', include(v1_post_urls))
)
