from api.views import get_token, get_cookie
from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from notify.api import NotificationViewSet
from push.api import PushSessionList
import api
from website.views import PostsListView, PostFormView, CommentFormView, \
    PostDetailView, ProfileDetailView, ProfileEditView, CategoryListView
from website.models import Post, UserProfile
from django.contrib import admin
from invite_only.views import InviteCodeView
from website.api import PostList, PostDetail, PostCommentList, CategoryList, \
    CategoryDetail, UserList, UserDetail
from poll.api import SubmissionList, PollDetail, PollList, \
    VoteDetail, VoteList
from chat_server.api import ChatMessageList


admin.autodiscover()

post_detail = login_required(PostDetailView.as_view(model=Post))
post_list = login_required(PostsListView.as_view(model=Post))
post_form = login_required(PostFormView.as_view())
profile_detail = login_required(ProfileDetailView.as_view(model=UserProfile))
profile_update = login_required(ProfileEditView.as_view())
invite_form = login_required(InviteCodeView.as_view())
comment_form = login_required(CommentFormView.as_view())
category_list = login_required(CategoryListView.as_view())

v1_post_urls = patterns(
    '',
    url(r'^posts/$',
        PostList.as_view(),
        name='post-list'),
    url(r'^posts/(?P<pk>\d+)/$',
        PostDetail.as_view(),
        name='post-detail'),
    url(r'^posts/(?P<pk>\d+)/comments/$',
        PostCommentList.as_view(),
        name='post-comment-list')
)

v1_poll_urls = patterns(
    '',
    url(r'^polls/$',
        PollList.as_view(),
        name='poll-list'),
    url(r'^polls/(?P<stub>[A-Za-z0-9_]+)/$',
        PollDetail.as_view(),
        name='poll-detail'),
    url(r'^polls/(?P<stub>[A-Za-z0-9_]+)/submissions/$',
        SubmissionList.as_view(),
        name='submission-list'),
)

v1_push_urls = patterns(
    '',
    url(r'^push/$',
        PushSessionList.as_view(),
        name='push-session-list'),
)

v1_category_urls = patterns(
    '',
    url(r'^categories/$',
        CategoryList.as_view(),
        name='category-list'),
    url(r'^categories/(?P<pk>\d+)/$',
        CategoryDetail.as_view(),
        name='category-detail'),
)

v1_user_urls = patterns(
    '',
    url(r'^users/$',
        UserList.as_view(),
        name='user-list'),
    url(r'^users/(?P<username>[A-Za-z0-9_]+)/$',
        UserDetail.as_view(),
        name='user-detail'),
)

v1_notification_urls = patterns(
    '',
    url(r'^notifications/$',
        NotificationViewSet.as_view(),
        name='notifications')
)

v1_chat_urls = patterns(
    '',
    url(r'^chat/messages/$',
        ChatMessageList.as_view(),
        name='chat-messages'),
)

v1_vote_urls = patterns(
    '',
    url(r'^votes/$',
        VoteList.as_view(),
        name='vote-list'),
    url(r'^votes/(?P<pk>\d+)/$',
        VoteDetail.as_view(),
        name='vote-detail')
)

notification_list = NotificationViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
notification_detail = NotificationViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = patterns(
    '',
    url(r'^accounts/', include('allauth.urls')),
    url(r'^auth/', include('django.contrib.auth.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url('^_ah/warmup$', 'website.views.warmup'),

    # API
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^api/v1/', include(v1_post_urls)),
    url(r'^api/v1/', include(v1_user_urls)),
    url(r'^api/v1/', include(v1_poll_urls)),
    url(r'^api/v1/', include(v1_chat_urls)),
    url(r'^api/v1/', include(v1_category_urls)),
    url(r'^api/v1/', include(v1_vote_urls)),
    url(r'^api/v1/', include(v1_push_urls)),
    # TODO(JoshNang) match other api urls.
    url('^api/v1/notifications/$', notification_list),
    url('^api/v1/notifications/(?P<pk>\d+)/$',
        notification_detail),
    url('^api/v1/check_in/$', api.views.check_in),

    url(r'^api/v1/token/', get_token),
    url(r'^api/cookie/', get_cookie),
    url(r'^_ah/channel/connected', 'push.views.connect'),
    url(r'^_ah/channel/disconnected',
        'push.views.disconnect'),
    # url(r'^_ah/channel/receive', 'chat_server.views.receive'),
)
