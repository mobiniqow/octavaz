from datetime import timedelta
from django.utils import timezone

class WalletTransactionFilter:
    @staticmethod
    def filter_daily():
        """
        فیلتر شارژهای روزانه
        """
        today = timezone.now().date()
        return SMS.objects.filter(sent_at__date=today)

    @staticmethod
    def filter_weekly():
        """
        فیلتر شارژهای هفتگی
        """
        start_of_week = timezone.now() - timedelta(days=timezone.now().weekday())
        return SMS.objects.filter(sent_at__gte=start_of_week)

    @staticmethod
    def filter_monthly():
        """
        فیلتر شارژهای ماهانه
        """
        start_of_month = timezone.now().replace(day=1)
        return SMS.objects.filter(sent_at__gte=start_of_month)
