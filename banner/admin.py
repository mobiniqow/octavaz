from django.contrib import admin

# Register your models here.
from .models import Banner

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    pass