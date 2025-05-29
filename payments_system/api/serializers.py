from rest_framework import serializers

from payments.models import (
    PAYMENT_AMOUNT_DECIMAL_PLACES,
    PAYMENT_AMOUNT_MAX_DIGITS,
    Payment,
)
from organizations.models import (
    ORGANIZATION_INN_MAX_LENGTH,
    Organization,
)


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            'operation_id',
            'id',
            'amount',
            'payer_inn',
            'document_number',
            'document_date',
        )

    def validate_payer_inn(self, value):
        if not Organization.objects.filter(inn=value).exists():
            raise serializers.ValidationError(
                'Организации с таким ИНН не найдена',
            )
        return value