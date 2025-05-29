import uuid

from django.db import models

from organizations.models import (
    Organization,
    ORGANIZATION_INN_MAX_LENGTH,
)

PAYMENT_AMOUNT_MAX_DIGITS = 14
PAYMENT_AMOUNT_DECIMAL_PLACES = 2


class Payment(models.Model):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name='payments',
    )
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4,
        editable=False,
    )
    amount = models.DecimalField(
        'Сумма',
        max_digits=PAYMENT_AMOUNT_MAX_DIGITS,
        decimal_places=PAYMENT_AMOUNT_DECIMAL_PLACES,
    )
    payer_inn = models.CharField(max_length=ORGANIZATION_INN_MAX_LENGTH, blank=True, null=True)
    document_number = models.CharField(max_length=50, blank=True, null=True)
    document_date = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.organization}: {self.amount}'

    def __repr__(self) -> str:
        return f'{self.id}'