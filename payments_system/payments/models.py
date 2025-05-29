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
        verbose_name='Организация',
    )
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4,
        editable=False,
    )
    operation_id = models.UUIDField('ID операции')
    amount = models.DecimalField(
        'Сумма',
        max_digits=PAYMENT_AMOUNT_MAX_DIGITS,
        decimal_places=PAYMENT_AMOUNT_DECIMAL_PLACES,
    )
    payer_inn = models.CharField('ИНН плательщика', max_length=ORGANIZATION_INN_MAX_LENGTH)
    document_number = models.CharField('Номер документа', max_length=50)
    document_date = models.DateTimeField('Дата документа')

    def __str__(self) -> str:
        return f'{self.organization}: {self.amount}'

    def __repr__(self) -> str:
        return f'{self.id}'