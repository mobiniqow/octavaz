from django.contrib import admin
from .models import Train, Feedback

@admin.register(Train)
class TrainAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'course', 'training_type', 'can_delete')
    list_filter = ('training_type', 'can_delete')
    search_fields = ('descriptions', 'user__username', )
    list_editable = ('can_delete', 'training_type')
    ordering = ('-id',)
    readonly_fields = ('media_file',)
    fieldsets = (
        ("General Information", {
            'fields': ('descriptions', 'course', 'user', 'training_type', 'can_delete')
        }),
        ("Media", {
            'fields': ('media_file',)
        }),
    )

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'train', 'master', 'master_point', 'created_at', 'updated_at')
    list_filter = ('master_point', 'created_at')
    search_fields = ('description', 'master__username', 'train__id')
    ordering = ('-created_at',)
    readonly_fields = ('media_file', 'created_at', 'updated_at')
    fieldsets = (
        ("General Information", {
            'fields': ('train', 'master', 'description', 'master_point')
        }),
        ("Media", {
            'fields': ('media_file',)
        }),
        ("Timestamps", {
            'fields': ('created_at', 'updated_at')
        }),
    )
