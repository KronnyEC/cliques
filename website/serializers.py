from poll.serializers import VoteSerializer
from rest_framework import serializers
from website.models import UserProfile, Post, Comment, Category


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.HyperlinkedIdentityField(
        'posts', view_name='userpost-list', lookup_field='username')
    user_votes = serializers.SerializerMethodField('get_user_votes')

    class Meta:
        model = UserProfile
        fields = (
            'id', 'username', 'profile_pic', 'email', 'first_name',
            'last_name', 'poll_votes', 'user_votes', 'last_updated'
        )

    def get_user_votes(self, obj):
        return VoteSerializer(obj.user_votes.all(), many=True,
                              read_only=True).data


class PostSerializer(serializers.ModelSerializer):
    url = serializers.URLField(source='url', required=False)
    user = UserSerializer(read_only=True)
    comment_set = serializers.SerializerMethodField('get_comment_set')

    class Meta:
        model = Post
        fields = ('id', 'submitted', 'edited', 'user', 'title', 'url', 'type',
                  'category', 'comment_set')
        depth = 1

    def get_comment_set(self, obj):
        return CommentSerializer(obj.comment_set.all(), many=True,
                                 read_only=True).data


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    username = serializers.SerializerMethodField('get_username')

    class Meta:
        model = Comment
        fields = ('id', 'user', 'text', 'submitted',
                  'edited', 'post', 'username')

    def get_username(self, obj):
        return obj.user.username


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'created_by', 'name', 'color')
