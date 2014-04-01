from django.contrib import admin
from website.models import Comment, Post
from website.models import UserProfile


admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(UserProfile)