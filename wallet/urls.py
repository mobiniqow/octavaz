from django.urls import path
from . import views

urlpatterns = [
    # API برای شروع پرداخت
    path('payment/start/', views.start_payment, name='start_payment'),

    # API برای تایید پرداخت پس از برگشت از زرین‌پال
    path('payment/verify/', views.verify_payment, name='verify_payment'),

    # API برای مشاهده تراکنش‌ها
    path('payment/transactions/', views.get_transactions, name='get_transactions'),

    # API برای دریافت URL پرداخت زرین‌پال
    path('payment/url/', views.get_payment_url, name='get_payment_url'),
    path('user-transactions/', views.CourseIncomingView.as_view(), name='user-transactions')
]
