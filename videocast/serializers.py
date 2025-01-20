from rest_framework import serializers

from videocast.models import VideoCast, Comment


class VideoCastSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoCast
        fields = ['id', 'title', 'descripcion', 'media', 'url', 'created_at', 'updated_at', 'slug']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'video', 'content', 'created_at']
