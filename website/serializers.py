from rest_framework import serializers
from website.models import UserProfile, Post, Comment


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.HyperlinkedIdentityField(
        'posts', view_name='userpost-list', lookup_field='username')

    class Meta:
        model = UserProfile
        fields = ('username', 'profile_pic', 'email', 'first_name', 'last_name')


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('submitted', 'edited', 'user', 'title', 'text', 'type',
                  'thumbnail')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('user', 'text', 'submitted', 'edited', 'post')