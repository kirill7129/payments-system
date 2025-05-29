from django.urls import path

from api.views import PaymentWebhookAPIView

urlpatterns = [
    path('webhook/bank/', PaymentWebhookAPIView.as_view(), name='webhook'),
]