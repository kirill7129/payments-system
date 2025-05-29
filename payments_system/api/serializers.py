from rest_framework import serializers

from payments.models import Payment
from organizations.models import Organization


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
        read_only_fields = ('organization',)

    def validate_payer_inn(self, value: str):
        if not Organization.objects.filter(inn=value).exists():
            raise serializers.ValidationError(
                'Организация с таким ИНН не найдена',
            )
        return value
    

class OrganizationBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = (
            'inn',
            'balance',
        )
        read_only_fields = fields