from django.contrib import admin
from .models import Transaction, Payment


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'transaction_type', 'status', 'timestamp', 'authority')
    list_filter = ('transaction_type', 'status', 'timestamp')
    search_fields = ('user__username', 'authority', 'message')
    ordering = ('-timestamp',)
    fieldsets = (
        (None, {
            'fields': ('user', 'amount', 'transaction_type', 'status', 'timestamp', 'authority', 'message')
        }),
    )
    readonly_fields = ('timestamp',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'cart', 'transaction', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'transaction__authority')
    ordering = ('-created_at',)
    fieldsets = (
        (None, {
            'fields': ('user', 'cart', 'transaction', 'payment_url', 'status', 'created_at')
        }),
    )
    readonly_fields = ('created_at',)
