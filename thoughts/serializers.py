from rest_framework import serializers
from django.conf import settings

from .models import Post
from profiles.serializers import PublicProfileSerializer


class PostActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    content = serializers.CharField(allow_blank=True, required=False)

    def validate_actions(self, value):
        value = value.lower().strip()
        if not value in settings.POST_ACTION_OPTIONS:
            raise serializers.ValidationError("Некорректное действие")
        return value

class PostCreateSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    user = PublicProfileSerializer(source="user.profile", read_only=True)

    class Meta:
        model = Post
        fields = ['user', 'id', 'content', 'likes', 'timestamp']

    def get_likes(self, obj):
        return obj.likes.count()

    def validate_content(self, value):
        if len(value) > settings.MAX_POST_LENGTH:
            raise serializers.ValidationError("Слишком длинный пост")
        return value

    # def get_user(self, obj):
    #     return obj.user.id


class PostSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    user = PublicProfileSerializer(source="user.profile", read_only=True)
    parent = PostCreateSerializer(read_only=True)

    class Meta:
        model = Post
        fields = [
            'user', 
            'id', 
            'content', 
            'likes', 
            'is_repost', 
            'parent', 
            'timestamp'
            ]

    def get_likes(self, obj):
        return obj.likes.count()


    