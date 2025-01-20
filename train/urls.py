from django.urls import path
from .views import TrainListView, TrainDetailView

urlpatterns = [
    # لیست تمرینات و ارسال تمرین جدید
    path('trains/', TrainListView.as_view(), name='train-list'),

    # مشاهده جزئیات تمرین خاص
    path('trains/<int:pk>/', TrainDetailView.as_view(), name='train-detail'),

]
