from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'created_at', 'amount_display']
    list_filter = ['created_at']
