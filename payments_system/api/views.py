from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.db.models import F
from rest_framework.request import HttpRequest

from api.serializers import (
    PaymentSerializer,
    OrganizationBalanceSerializer,
)
from payments.models import BalanceLog, Payment
from organizations.models import Organization


class PaymentWebhookAPIView(APIView):
    def post(self, request: HttpRequest) -> Response:
        serializer = PaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        operation_id = data['operation_id']

        if Payment.objects.filter(operation_id=operation_id).exists():
            return Response(
                {'detail': 'Платеж уже обработан'},
                status=status.HTTP_200_OK,
            )
        
        with transaction.atomic():
            try:
                organization = Organization \
                    .objects \
                    .select_for_update() \
                    .get(inn=data['payer_inn'])
            except Organization.DoesNotExist:
                return Response(
                    {
                        'detail': 'Организация с таким ИНН не найдена'
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
            

            payment = Payment.objects.create(
                **data, 
                organization=organization
            )

            organization.refresh_from_db()
            balance_before = organization.balance

            organization.balance = F('balance') + payment.amount
            organization.save()

            organization.refresh_from_db()
            balance_after = organization.balance

            BalanceLog.objects.create(
                payment=payment,
                before=balance_before,
                after=balance_after,
            )

        return Response(
            {'detail': 'Платеж успешно обработан'},
            status=status.HTTP_201_CREATED,
        )
    

class OrganizationBalanceAPIView(APIView):
    def get(self, request: HttpRequest, inn: str) -> Response:
        try:
            organization = Organization.objects.get(inn=inn)
        except Organization.DoesNotExist:
            return Response(
                {'detail': 'Организации с таким ИНН не существует'},
                status=status.HTTP_404_NOT_FOUND,
            )
        
        serializer = OrganizationBalanceSerializer(
            organization
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
