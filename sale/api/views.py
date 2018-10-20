from rest_framework.generics import RetrieveAPIView, ListAPIView, UpdateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response

from .serializers import PaymentSerializerList, PaymentSerializerNote
from sale.models import Payment

class PaymentAPIRetriList(ListAPIView):
    serializer_class = PaymentSerializerList

    def get_queryset(self):
        new_query = Payment.objects.filter(noted=False)
        return new_query

class PaymentNoteUpdateAPInote(UpdateAPIView):
    serializer_class = PaymentSerializerNote
    queryset = Payment.objects.all()