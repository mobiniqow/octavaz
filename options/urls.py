from django.urls import path
from .views import OptionsAPIView

urlpatterns = [
    path('api/options/', OptionsAPIView.as_view(), name='options-api'),
]
