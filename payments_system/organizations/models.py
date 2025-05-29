import uuid

from django.db import models

ORGANIZATION_INN_MAX_LENGTH = 12

BALANCE_MAX_DIGITS = 14
BALANCE_DECIMAL_PLACES = 2


class Organization(models.Model):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4,
        editable=False,
    )
    inn = models.CharField(
        'ИНН',
        max_length=ORGANIZATION_INN_MAX_LENGTH,
        unique=True,
    )
    balance = models.DecimalField(
        'Баланс',
        max_digits=BALANCE_MAX_DIGITS,
        decimal_places=BALANCE_DECIMAL_PLACES,
    )

    def __str__(self) -> str:
        return self.inn

    def __repr__(self) -> str:
        return f'{self.id}'