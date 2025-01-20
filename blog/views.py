# blog/views.py
from rest_framework import generics
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django_filters.rest_framework import DjangoFilterBackend
from .filters import PostFilter
from rest_framework import filters

class PostListView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = PostFilter

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def retrieve(self, request, *args, **kwargs):
        # گرفتن پست و نمایش جزئیات به همراه کامنت‌ها و بنرها
        post = self.get_object()
        serializer = self.get_serializer(post)
        return Response(serializer.data)

@api_view(['POST'])
def add_comment(request, pk):
    post = Post.objects.get(pk=pk)
    if post.allow_comments:  # بررسی اینکه آیا اجازه ارسال کامنت برای این پست وجود دارد
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    return Response({"detail": "Comments are not allowed for this post."}, status=400)
