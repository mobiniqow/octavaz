import django_filters
from .models import Transaction
from django.utils import timezone
from datetime import timedelta

class WalletTransactionFilter(django_filters.FilterSet):
    # فیلتر برای تراکنش‌های روزانه
    daily = django_filters.DateTimeFilter(field_name='timestamp', lookup_expr='gte', method='filter_daily')
    # فیلتر برای تراکنش‌های هفتگی
    weekly = django_filters.DateTimeFilter(field_name='timestamp', lookup_expr='gte', method='filter_weekly')
    # فیلتر برای تراکنش‌های ماهانه
    monthly = django_filters.DateTimeFilter(field_name='timestamp', lookup_expr='gte', method='filter_monthly')

    class Meta:
        model = Transaction
        fields = ['daily', 'weekly', 'monthly']

    def filter_daily(self, queryset, name, value):
        today = timezone.now().date()
        return queryset.filter(timestamp__date=today)

    def filter_weekly(self, queryset, name, value):
        # فیلتر برای تراکنش‌های هفته جاری
        start_of_week = timezone.now() - timedelta(days=timezone.now().weekday())  # شروع هفته
        return queryset.filter(timestamp__gte=start_of_week)

    def filter_monthly(self, queryset, name, value):
        # فیلتر برای تراکنش‌های ماه جاری
        start_of_month = timezone.now().replace(day=1)
        return queryset.filter(timestamp__gte=start_of_month)
