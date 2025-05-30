import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from payments.models import (
    Payment,
    BalanceLog,
)
from organizations.models import Organization


@pytest.mark.django_db
class TestPaymentWebhookAPIView():
    URL = reverse('webhook')

    def test_payment_success(
            self,
            api_client: APIClient, 
            valid_payload: dict, 
            organization: Organization
        ):
        response = api_client.post(
            self.URL,
            data=valid_payload,
            format='json',
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['detail'] == 'Платеж успешно обработан'

        payment = Payment.objects.get(
            operation_id=valid_payload['operation_id'],
        )
        assert payment.amount == 150
        assert payment.organization == organization

        organization.refresh_from_db()
        assert organization.balance == 150

        balance_log = BalanceLog.objects.get(payment=payment)
        assert balance_log.before == 0
        assert balance_log.after == 150

    def test_duplicate_payment(
            self,
            api_client: APIClient, 
            valid_payload: dict, 
            organization: Organization
        ):
        api_client.post(
            self.URL,
            data=valid_payload,
            format='json',
        )

        response = api_client.post(
            self.URL,
            data=valid_payload,
            format='json',
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data['detail'] == 'Платеж уже обработан'

    def test_payment_invalid_inn(self, api_client: APIClient):
        payload = {
        'operation_id': 'ccf0a86d-041b-4991-bcf7-e2352f7b8a4a',
        'amount': 150,
        'payer_inn': '12345678903',
        'document_number': 'PAY-328',
        'document_date': '2024-04-27T21:00:00Z',
        }

        response = api_client.post(
            self.URL,
            data=payload,
            format='json',
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['payer_inn'][0] == 'Организация с таким ИНН не найдена'


@pytest.mark.django_db
class TestOrganizationBalanceAPIView():
    def test_get_organization_balance_success(
            self, 
            api_client: APIClient, 
            organization: Organization
        ):
        url = reverse('balance', kwargs={'inn': organization.inn})

        response = api_client.get(
            url
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data['inn'] == organization.inn
        assert response.data['balance'] == '0.00'

    def test_get_non_existing_organization_balance(self, api_client: APIClient):
        url = reverse('balance', kwargs={'inn': '123'})

        response = api_client.get(
            url
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['detail'] == 'Организации с таким ИНН не существует'

        