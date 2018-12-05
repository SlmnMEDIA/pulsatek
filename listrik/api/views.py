from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView, GenericAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from datetime import date, datetime

from listrik.models import Operator, Product, Transaction

from .serializers import (
#     OperatorListSerializer,
#     OperatorDetailSerializer,
    ProductListSerializer,
    ProductDetailSerializer,
    TransactionSerializer,
    TransactionPostSerializer,
    TransactionDetailSerializer,
    TransactionResposneSerializer,
    TeleTrxStatusSerializer,
)

from .paginators import StandardResultsSetPagination

from core.api.serializers import StatusTransactionSrializer as StatusTrx
from core.models import StatusTransaction

# class OperatorListView(ListAPIView):
#     queryset = Operator.onactive.all()
#     serializer_class = OperatorListSerializer
#     permission_classes = [
#         IsAuthenticated
#     ]


# class OperatorDetailView(RetrieveAPIView):
#     queryset = Operator.objects.all()
#     serializer_class = OperatorDetailSerializer
#     permission_classes = [
#         IsAuthenticated
#     ]


class ProductListView(ListAPIView):
    serializer_class = ProductListSerializer
    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self, *args, **kwargs):
        query = Product.objects.all()
        operator = self.request.GET.get('op', None)
        if operator:
            query = query.filter(operator__id=operator)

        return query

class ProductNoAListView(ListAPIView):
    serializer_class = ProductListSerializer

    def get_queryset(self, *args, **kwargs):
        query = Product.objects.all()
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

class ProductNoADetailView(RetrieveAPIView):
    serializer_class = ProductDetailSerializer
    queryset = Product.objects.all()


class TransactionCreateView(CreateModelMixin, GenericAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        try :
            product_obj = Product.objects.get(id=request.data['product'])
        except:
            status_obj = StatusTransaction.objects.get(code='10')
            return Response(StatusTrx(status_obj).data)

        trx_objs = Transaction.objects.filter(product=product_obj, phone=request.data['phone'], timestamp__date=date.today(), record__success=True, record__debit=0)
        if trx_objs.exists():
            status_obj = StatusTransaction.objects.get(code='20')
            return Response(StatusTrx(status_obj).data)

        
        if not (request.user.saldo + request.user.limit > product_obj.price) :
            status_obj = StatusTransaction.objects.get(code='30')
            return Response(StatusTrx(status_obj).data)

        postserializer = self.get_serializer_class()
        trxpost = postserializer(data=request.data)
        if trxpost.is_valid():
            instance = trxpost.save(buyer=request.user)
            instance.refresh_from_db()
            trx = Transaction.objects.get(id=instance.id)
            resTrx = TransactionResposneSerializer(trx)
            return Response(resTrx.data)

        return Response(serializer_creator.errors, status=status.HTTP_400_BAD_REQUEST)


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
            product_obj = Product.objects.get(product_code=request.data['product_code'])
            output['product'] = ProductDetailSerializer(product_obj).data
        except :
            status_obj = StatusTransaction.objects.get(code='10')
            output['status'] = StatusTrx(status_obj).data
            return Response(output)

        request.data['product'] = product_obj.id

        trx = Transaction.objects.filter(product=product_obj, phone=request.data['phone'], timestamp__date=date.today(), record__success=True, record__debit=0)
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
            user_obj = request.user
            user_obj.refresh_from_db()
            output['saldo'] = user_obj.saldo
            return Response(output)

        return Response(serializer_creator.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionDetailSerApi(RetrieveAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionDetailSerializer
    permission_classes = [
        IsAuthenticated,
    ]

class TransactionListApiView(ListAPIView):
    serializer_class = TransactionResposneSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        query = Transaction.objects.filter(t_notive=False)
        return query


class TeleTrxStatusRetryView(RetrieveUpdateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TeleTrxStatusSerializer