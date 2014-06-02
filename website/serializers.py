from rest_framework import serializers
from website.models import UserProfile, Post, Comment, Category


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.HyperlinkedIdentityField(
        'posts', view_name='userpost-list', lookup_field='username')

    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'profile_pic', 'email',
                  'first_name', 'last_name')


class PostSerializer(serializers.ModelSerializer):
    comment_count = serializers.Field(source='comment_set.count')
    url = serializers.URLField(source='url', required=False)
    comment_set = serializers.RelatedField(source='comment_set',
                                           read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'submitted', 'edited', 'user', 'title', 'url', 'type',
                  'category', 'comment_set')
        depth = 1


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'user', 'text', 'submitted', 'edited', 'post')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('created_by', 'name', 'color')
