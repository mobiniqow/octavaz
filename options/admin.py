from django.contrib import admin
from .models import Options


class OptionsAdmin(admin.ModelAdmin):
    # نمایش فیلدهای مدل در فرم مدیریت
    fields = ['logo', 'intro_video', 'intro_text']

    # محدود کردن دکمه افزودن شیء جدید
    def has_add_permission(self, request):
        # اگر شیء‌ای وجود دارد، اجازه افزودن نده
        return not Options.objects.exists()

    # جلوگیری از حذف اشیاء
    def has_delete_permission(self, request, obj=None):
        return False


# ثبت مدل در پنل ادمین
admin.site.register(Options, OptionsAdmin)
