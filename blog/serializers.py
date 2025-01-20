# blog/serializers.py
from rest_framework import serializers
from .models import Post, Category, Hashtag, Comment, BannerImage

class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ('id', 'name')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')

    ref_name = 'BlogCategorySerializer'
class BannerImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BannerImage
        fields = ('id', 'image', 'order')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'name', 'email', 'content', 'created_at')

class PostSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    hashtags = HashtagSerializer(many=True)
    comments = CommentSerializer(many=True, read_only=True)
    banner_images = BannerImageSerializer(many=True, read_only=True)  # اضافه کردن بنرها

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'category', 'hashtags', 'comments', 'banner_images', 'created_at', 'updated_at')
