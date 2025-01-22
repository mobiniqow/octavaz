from django.contrib import admin
from .models import Artist, ArtistTransaction


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'instrument')
    search_fields = ('name', 'instrument')
    ordering = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'instrument', 'bio')
        }),
    )
@admin.register(ArtistTransaction)
class ArtistTransactionAdmin(admin.ModelAdmin):
    pass
