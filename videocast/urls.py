from django.urls import path
from .views import VideoCastListView, VideoCastDetailView, VideoCastCreateView, CommentCreateView

urlpatterns = [
    # VideoCast endpoints
    path('videocasts/', VideoCastListView.as_view(), name='video-list'),
    path('videocasts/<slug:slug>/', VideoCastDetailView.as_view(), name='video-detail'),
    path('videocasts/create/', VideoCastCreateView.as_view(), name='video-create'),

    # Comment endpoints
    path('videocasts/<slug:video_slug>/comments/', CommentCreateView.as_view(), name='comment-create'),
]
