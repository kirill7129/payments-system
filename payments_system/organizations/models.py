import uuid

from django.db import models


class Organization(models.Model):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4,
    )
    inn = models.CharField(
        'ИНН',
        max_length=12,
        unique=True,
    )
    balance = models.DecimalField(
        'Баланс',
        max_digits=14,
        decimal_places=2,
    )

    def __str__(self) -> str:
        return self.inn
