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
from payments.models import Payment
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
            organization = Organization \
                .objects \
                .select_for_update() \
                .get(inn=data['payer_inn'])

            payment = Payment.objects.create(
                **data, 
                organization=organization
            )

            organization.balance = F('balance') + payment.amount
            organization.save()

        return Response(
            {'detail': 'Платеж успешно обработан'},
            status=status.HTTP_201_CREATED,
        )
    

class OrganizationBalanceAPIView(APIView):
    def get(self, request: HttpRequest, inn: str) -> Response:
        try:
            org = Organization.objects.get(inn=inn)
        except Organization.DoesNotExist:
            return Response(
                {'detail': 'Организации с таким ИНН не существует'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        serializer = OrganizationBalanceSerializer(
            org
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
