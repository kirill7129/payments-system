from django.urls import path

from api.views import (
    PaymentWebhookAPIView,
    OrganizationBalanceAPIView,
)

urlpatterns = [
    path('webhook/bank/', PaymentWebhookAPIView.as_view(), name='webhook'),
    path('organizations/<str:inn>/balance/', OrganizationBalanceAPIView.as_view(), name='balance'),
]