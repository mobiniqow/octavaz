# blog/urls.py
from django.urls import path
from .views import PostListView, PostDetailView, CommentCreateView

urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('comments/', CommentCreateView.as_view(), name='comment-create'),
]
