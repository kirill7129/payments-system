from django.contrib import admin

from payments.models import (
    Payment,
    BalanceLog,
)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'amount',
        'payer_inn',
        'organization',
        'document_number',
        'document_date',
    )


@admin.register(BalanceLog)
class BalanceLogAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'payment',
        'before',
        'after',
        'timestamp',
    )
