from django.contrib import admin

from payments.models import Payment


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
