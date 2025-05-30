import pytest
from rest_framework.test import APIClient

from organizations.models import Organization


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def organization() -> Organization:
    return Organization.objects.create(
        inn='1234567890',
        balance=0,
    )


@pytest.fixture
def valid_payload() -> dict:
    return {
        'operation_id': 'ccf0a86d-041b-4991-bcf7-e2352f7b8a4a',
        'amount': 150,
        'payer_inn': '1234567890',
        'document_number': 'PAY-328',
        'document_date': '2024-04-27T21:00:00Z',
    }