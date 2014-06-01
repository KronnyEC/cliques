from django.db.models import Count
from rest_framework import generics, permissions

from website.serializers import UserSerializer, PostSerializer, \
    CommentSerializer
from website.models import UserProfile, Post, Comment


class UserDetail(generics.RetrieveAPIView):
    model = UserProfile
    serializer_class = UserSerializer
    permission_classes = [
        permissions.AllowAny
    ]


class PostList(generics.ListCreateAPIView):
    model = Post
    serializer_class = PostSerializer
    permission_classes = [
        permissions.AllowAny
    ]
    paginate_by = 10
    paginate_by_param = 'page_size'
    max_paginate_by = 100

    def get_queryset(self):
        queryset = Post.objects.annotate(comment_count=Count('comment'))
        return queryset


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Post
    serializer_class = PostSerializer
    permission_classes = [
        permissions.AllowAny
    ]

    def get_queryset(self):
        queryset = super(PostList, self).get_queryset()
        queryset = queryset.annotate(comment_count=Count('comment_set'))
        return queryset


class UserPostList(generics.ListAPIView):
    model = Post
    serializer_class = PostSerializer
    paginate_by = 10
    paginate_by_param = 'page_size'
    max_paginate_by = 100

    def get_queryset(self):
        queryset = super(UserPostList, self).get_queryset()
        return queryset.filter(author__username=self.kwargs.get('username'))


class CommentList(generics.ListCreateAPIView):
    model = Comment
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.AllowAny
    ]


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Comment
    serializer_class = CommentSerializer
    paginate_by = 100
    paginate_by_param = 'page_size'
    max_paginate_by = 1000
    permission_classes = [
        permissions.AllowAny
    ]


class PostCommentList(generics.ListAPIView):
    model = Comment
    serializer_class = CommentSerializer
    paginate_by = 100
    paginate_by_param = 'page_size'
    max_paginate_by = 1000

    def get_queryset(self):
        queryset = super(PostCommentList, self).get_queryset()
        return queryset.filter(post__pk=self.kwargs.get('pk'))


# class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
#     model = UserProfile
#     serializer_class = ProfileSerializer
#     permission_classes = [
#         permissions.AllowAny
#     ]
