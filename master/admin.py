from django.contrib import admin
from .models import Artist, ArtistTransaction
from .models import CourseMasterCertificate
from django.utils.translation import gettext_lazy as _

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'instrument', 'master')
    search_fields = ('name', 'instrument', 'master__username')
    list_filter = ('instrument',)
    ordering = ('name',)
    fieldsets = (
        ("General Information", {
            'fields': ('name', 'instrument', 'bio', 'image', 'master')
        }),
    )

@admin.register(ArtistTransaction)
class ArtistTransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'artist', 'status', 'price', 'price_type', 'created_at')
    list_filter = ('status', 'price_type', 'created_at')
    search_fields = ('artist__name',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    fieldsets = (
        ("Transaction Details", {
            'fields': ('artist', 'status', 'price', 'price_type')
        }),
        ("Timestamps", {
            'fields': ('created_at',)
        }),
    )



class CourseMasterCertificateAdmin(admin.ModelAdmin):
    list_display = ('id', 'course',  'issued_to', 'state', 'issued_at')
    list_filter = ('state', 'course',  'issued_to')
    search_fields = ('id', 'course__name', 'issued_by__username', 'issued_to__username')
    ordering = ('-issued_at',)
    actions = ['approve_certificates', 'reject_certificates']

    # برای انتخاب اینکه کدام فیلدها در فرم ادمین نمایش داده شود
    fields = ('course', 'certificate', 'state',  'issued_to', 'issued_at')
    readonly_fields = ('id', 'issued_at')  # `id` و `issued_at` قابل ویرایش نباشند

    # روش برای تایید یا رد سرتیفیکیت‌ها
    def approve_certificates(self, request, queryset):
        queryset.update(state='approved')
        self.message_user(request, _("Certificates successfully approved."))

    def reject_certificates(self, request, queryset):
        queryset.update(state='rejected')
        self.message_user(request, _("Certificates successfully rejected."))

    # برای نمایش آی‌دی به صورت خوانا
    def get_readonly_fields(self, request, obj=None):
        if obj:  # در صورتی که سرتیفیکیت موجود باشد (برای ویرایش)
            return self.readonly_fields + ('certificate',)
        return self.readonly_fields


admin.site.register(CourseMasterCertificate, CourseMasterCertificateAdmin)