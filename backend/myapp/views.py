from django.http import JsonResponse, HttpResponseNotFound
from django.views.decorators.http import require_http_methods
from .models import Payment
from .serializers import PaymentSerializer

def index(request):
    return JsonResponse({"status": "ok", "service": "backend-myapp"})

@require_http_methods(["GET"])
def payment_by_swift(request, swift_code):
    """Return payment details and related transactions for a given swift code."""
    try:
        payment = Payment.objects.get(swift_code=swift_code)
    except Payment.DoesNotExist:
        return HttpResponseNotFound('Swift code not found')

    serializer = PaymentSerializer(payment)
    response = JsonResponse(serializer.data, safe=False)
    # lightweight CORS for dev (adjust in production)
    response['Access-Control-Allow-Origin'] = '*'
    return response
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from .models import Payment, Transaction
from .serializers import PaymentSerializer, TransactionSerializer


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Provides list and detail endpoints for payments.
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    lookup_field = 'swift_code'  # allows /api/payments/<swift_code>/

    @action(detail=True, methods=['get'])
    def transactions(self, request, swift_code=None):
        payment = self.get_object()
        serializer = TransactionSerializer(payment.transactions.all(), many=True)
        return Response(serializer.data)


class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Provides list and detail endpoints for transactions.
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
