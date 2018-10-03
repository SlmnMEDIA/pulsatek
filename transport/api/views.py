from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from datetime import date, datetime

from transport.models import Operator, Product, Transaction
from .serializers import (
    OperatorListSerializer,
    OperatorDetailSerializer,
    ProductListSerializer,
    ProductDetailSerializer,
    TransactionSerializer,
    TransactionPostSerializer,
)

from core.api.serializers import StatusTransactionSrializer as StatusTrx
from core.models import StatusTransaction


class OperatorListView(ListAPIView):
    queryset = Operator.onactive.all()
    serializer_class = OperatorListSerializer
    permission_classes = [
        IsAuthenticated
    ]


class OperatorDetailView(RetrieveAPIView):
    queryset = Operator.objects.all()
    serializer_class = OperatorDetailSerializer
    permission_classes = [
        IsAuthenticated
    ]


class ProductListView(ListAPIView):
    serializer_class = ProductListSerializer
    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self, *args, **kwargs):
        query = Product.onactive.all()
        operator = self.request.GET.get('op', None)
        if operator:
            query = query.filter(operator__id=operator)

        return query


class ProductDetailView(RetrieveAPIView):
    serializer_class = ProductDetailSerializer
    queryset = Product.objects.all()
    permission_classes = [
        IsAuthenticated
    ]


class TransactionCreateView(CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [
        IsAuthenticated
    ]


class TransactionCreatePost(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request, format=None):
        output = {
            'status': None,
            'product': None,
            'trx': None
        }
        try:
            product_obj = Product.onactive.get(product_code=request.data['product_code'])
            output['product'] = ProductDetailSerializer(product_obj).data
        except :
            status_obj = StatusTransaction.objects.get(code='10')
            output['status'] = StatusTrx(status_obj).data
            return Response(output)

        request.data['product'] = product_obj.id

        trx = Transaction.objects.filter(product=product_obj, phone=request.data['phone'], timestamp__date=date.today(), record__success=True)
        if trx.exists():
            status_obj = StatusTransaction.objects.get(code='20')
            output['status'] = StatusTrx(status_obj).data
            return Response(output)

        if not (request.user.saldo + request.user.limit > product_obj.price) :
            status_obj = StatusTransaction.objects.get(code='30')
            output['status'] = StatusTrx(status_obj).data
            return Response(output)


        serializer_creator = TransactionPostSerializer(data=request.data, context={'request':request})
        if serializer_creator.is_valid():
            serializer_creator.save(buyer=request.user)
            output['trx'] = serializer_creator.data
            status_obj = StatusTransaction.objects.get(code='00')
            output['status'] = StatusTrx(status_obj).data
            return Response(output)

        return Response(serializer_creator.errors, status=status.HTTP_400_BAD_REQUEST)