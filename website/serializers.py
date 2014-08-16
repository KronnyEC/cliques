from rest_framework import serializers
from website.models import UserProfile, Post, Comment, Category


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.HyperlinkedIdentityField(
        'posts', view_name='userpost-list', lookup_field='username')

    class Meta:
        model = UserProfile
        fields = (
            'id', 'username', 'profile_pic', 'email', 'first_name',
            'last_name', 'poll_votes', 'user_votes', 'last_updated'
        )


class PostSerializer(serializers.ModelSerializer):
    url = serializers.URLField(source='url', required=False)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'submitted', 'edited', 'user', 'title', 'url', 'type',
                  'category', 'comment_set')
        depth = 1


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    username = serializers.SerializerMethodField('get_username')

    class Meta:
        model = Comment
        fields = ('id', 'user', 'text', 'submitted', 'edited', 'post', 'user_ob')

    def get_username(self, obj):
        return obj.user.username


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'created_by', 'name', 'color')
