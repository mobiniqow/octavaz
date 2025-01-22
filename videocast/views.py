from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import VideoCast, Comment
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from .serializers import VideoCastSerializer, CommentSerializer


class VideoCastListView(APIView):
    """
    List all video casts.
    """

    def get(self, request):
        videos = VideoCast.objects.all()
        serializer = VideoCastSerializer(videos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VideoCastDetailView(APIView):
    """
    Retrieve a specific video cast and its comments.
    """

    def get(self, request, slug):
        video = get_object_or_404(VideoCast, slug=slug)
        serializer = VideoCastSerializer(video)
        comments = Comment.objects.filter(video=video)
        comment_serializer = CommentSerializer(comments, many=True)
        data = serializer.data
        data['comments'] = comment_serializer.data
        return Response(data, status=status.HTTP_200_OK)


class VideoCastCreateView(APIView):
    """
    Create a new video cast.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        serializer = VideoCastSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class CommentCreateView(APIView):
    """
    Create a comment for a video.
    """
    permission_classes = [IsAuthenticated]  # دسترسی فقط برای کاربران احراز هویت شده

    def post(self, request, video_slug):
        # پیدا کردن ویدیو بر اساس slug
        video = get_object_or_404(VideoCast, slug=video_slug)

        # تنظیم داده‌ها: کاربر و ویدیو از منابع مرتبط گرفته می‌شوند
        data = {
            'video': video.id,  # ID ویدیو از URL
            'user': request.user.id,  # ID کاربر از request.user
            'content': request.data.get('content')  # محتوا از داده‌های درخواست
        }

        # سریالایزر برای اعتبارسنجی داده‌ها
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

