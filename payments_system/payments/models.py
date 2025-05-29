import uuid

from django.db import models

from organizations.models import Organization


class Payment(models.Model):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name='payments',
    )
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4,
    )
    amount = models.DecimalField(
        'Сумма',
        max_digits=14,
        decimal_places=2,
    )

    def __str__(self) -> str:
        return f'{self.organization}: {self.amount}'

    def __repr__(self) -> str:
        return f'{self.id}'