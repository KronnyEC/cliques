import logging

from rest_framework import generics, status
from rest_framework.response import Response

from website.serializers import UserSerializer, PostSerializer, \
    CommentSerializer, CategorySerializer
from website.models import UserProfile, Post, Comment, Category


logger = logging.getLogger(__name__)


class UserList(generics.ListCreateAPIView):
    model = UserProfile
    serializer_class = UserSerializer
    paginate_by = 25
    paginate_by_param = 'page_size'
    max_paginate_by = 100

    def get_queryset(self):
        return UserProfile.objects.all().order_by('-last_updated')


class UserDetail(generics.RetrieveAPIView):
    lookup_field = 'username'
    model = UserProfile
    serializer_class = UserSerializer


class PostList(generics.ListCreateAPIView):
    model = Post
    serializer_class = PostSerializer

    paginate_by = 10
    paginate_by_param = 'page_size'
    max_paginate_by = 100

    def create(self, request, *args, **kwargs):
        # TODO(pcsforeducation) this is a mess
        data = dict(request.DATA)

        # Get the category
        category_pk = int(data['category'][0])
        try:
            data['category'] = Category.objects.get(id=category_pk)
        except Category.DoesNotExist:
            return Response({'error': 'category does not exist'},
                            status=status.HTTP_400_BAD_REQUEST)
        data['title'] = data['title'][0]
        if data.get('url'):
            data['url'] = data['url'][0]
        data['user'] = request.user
        try:
            self.object = Post(**data)
            self.pre_save(self.object)
            self.object.save()
        except Exception:
            logger.exception('invalid form')
            return Response({'errors': 'Invalid form'},
                            status=status.HTTP_400_BAD_REQUEST)
        self.post_save(self.object, created=True)
        serializer = self.get_serializer(instance=self.object)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Post
    serializer_class = PostSerializer

    def get_queryset(self):
        queryset = super(PostDetail, self).get_queryset()
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


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Comment
    serializer_class = CommentSerializer
    paginate_by = 100
    paginate_by_param = 'page_size'
    max_paginate_by = 1000


class PostCommentList(generics.ListCreateAPIView):
    model = Comment
    serializer_class = CommentSerializer
    paginate_by = 100
    paginate_by_param = 'page_size'
    max_paginate_by = 1000

    def pre_save(self, obj):
        obj.user = self.request.user

    def get_queryset(self):
        queryset = super(PostCommentList, self).get_queryset()
        return queryset.filter(post__pk=self.kwargs.get('pk'))


class CategoryList(generics.ListCreateAPIView):
    model = Category
    serializer_class = CategorySerializer


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Category
    serializer_class = CategorySerializer
