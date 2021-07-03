from rest_framework import serializers
from django.conf import settings

from .models import Post


class PostActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()

    def validate_actions(self, value):
        value = value.lower().strip()
        if not value in settings.POST_ACTION_OPTIONS:
            raise serializers.ValidationError("Некорректное действие")
        return value

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['content']

    def validate_content(self, value):
        if len(value) > settings.MAX_POST_LENGTH:
            raise serializers.ValidationError("Короче, пожалста!")
        return value