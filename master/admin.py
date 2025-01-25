from django.contrib import admin
from .models import Artist, ArtistTransaction

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
