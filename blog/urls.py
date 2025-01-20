# blog/urls.py
from django.urls import path
from .views import PostListView, PostDetailView, add_comment

urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:pk>/comments/', add_comment, name='comment-create'),  # اضافه کردن کامنت
]
