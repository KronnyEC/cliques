from api.views import get_token, get_cookie
from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from notify.api import NotificationViewSet
from poll.views import PollDetailView, SubmissionFormView
from website.views import PostsListView, PostFormView, CommentFormView, \
    PostDetailView, ProfileDetailView, ProfileEditView, CategoryListView
from website.models import Post, UserProfile
from django.contrib import admin
from invite_only.views import InviteCodeView
from website.api import PostList, PostDetail, PostCommentList, CategoryList,\
    CategoryDetail, UserDetail
from poll.api import SubmissionList, SubmissionDetail, PollDetail, PollList, \
    VoteDetail, VoteList
from chat_server.api import ChatSessionList, ChatMessageList
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


admin.autodiscover()

post_detail = login_required(PostDetailView.as_view(model=Post))
post_list = login_required(PostsListView.as_view(model=Post))
post_form = login_required(PostFormView.as_view())
profile_detail = login_required(ProfileDetailView.as_view(model=UserProfile))
profile_update = login_required(ProfileEditView.as_view())
invite_form = login_required(InviteCodeView.as_view())
comment_form = login_required(CommentFormView.as_view())
category_list = login_required(CategoryListView.as_view())

v1_post_urls = patterns('',
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


v1_poll_urls = patterns('',
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

v1_category_urls = patterns('',
    url(r'^categories/$',
        CategoryList.as_view(),
        name='category-list'),
    url(r'^categories/(?P<pk>\d+)/$',
        CategoryDetail.as_view(),
        name='category-detail'),

)

v1_user_urls = patterns('',
    url(r'^users/(?P<username>[A-Za-z0-9_]+)/$',
        UserDetail.as_view(),
        name='user-detail'),
)

v1_notification_urls = patterns('',
    url(r'^notifications/$',
        NotificationViewSet.as_view(),
        name='notifications')
)

v1_chat_urls = patterns('',
    url(r'^chat/messages/$',
        ChatMessageList.as_view(),
        name='chat-messages'),
    url(r'^chat/sessions/$',
        ChatSessionList.as_view(),
        name='chat-sessions'),
)

v1_vote_urls = patterns('',
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
    url('^_ah/warmup$', 'website.views.warmup'),

    # url(r'^$', post_list, name='post_list', ),
    # url(r'^post/$', require_POST(post_form),
    #     name='post_form_view_url'),
    # url(r'^post/(?P<pk>[a-f\d]+)/$', post_detail, name='post_detail'),
    # url(r'^post/(?P<pk>[a-f\d]+)/comment/$',
    #     require_POST(comment_form),
    #     name='comment_form_view_url'),
    # url(r'^posts/', category_list),
    # url(r'^invite/$', invite_form, name='invite_form'),
    # url(r'^poll/(?P<stub>[\w_]+)/$', PollDetailView.as_view(),
    #     name='poll_submission'),
    # url(r'^poll/(?P<stub>[\w_]+)/submission/$', SubmissionFormView.as_view()),
    # url(r'^poll/(?P<poll_stub>[\w_]+)/(?P<submission_id>\d+)/vote/$',
    #     'poll.views.vote'),
    # url(r'^cron/poll/$', 'poll.views.cron'),
    # url(r'^users/$', 'website.views.user_redirect'),
    # url(r'^users/(?P<slug>\w+)/$', profile_update, name='profile_detail'),

    # Single root page
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='post_list', ),

    # API
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^api/v1/', include(v1_post_urls)),
    url(r'^api/v1/', include(v1_user_urls)),
    url(r'^api/v1/', include(v1_poll_urls)),
    url(r'^api/v1/', include(v1_chat_urls)),
    url(r'^api/v1/', include(v1_category_urls)),
    url(r'^api/v1/', include(v1_vote_urls)),
    #TODO(JoshNang) match other api urls.
    url('^api/v1/notifications/$', notification_list),
    url('^api/v1/notifications/(?P<pk>\d+)/$', notification_detail),

    url(r'^api/v1/token/', get_token),
    url(r'^api/cookie/', get_cookie),
    url(r'^_ah/channel/connected', 'chat_server.views.connect'),
    url(r'^_ah/channel/disconnected', 'chat_server.views.disconnect'),
    # url(r'^_ah/channel/receive', 'chat_server.views.receive'),
    # url(r'^chat/$', TemplateView.as_view(template_name="chat/chat.html")),
    # url(r'^chat/message/$', 'chat_server.views.receive'),
    # url(r'^chat/join_chat/$', 'chat_server.views.join_chat'),
    # url(r'^chat/leave_chat/$', 'chat_server.views.leave_chat'),
    # url(r'^chat/check_in/$', 'chat_server.views.check_in'),

    # Notifications
    # url(r'^notifications/$', 'notify.views.get_notifications'),
    # url('^notifications/$', notification_list),
    # url('^notifications/(?P<pk>\d+)/$', notification_detail),
)
