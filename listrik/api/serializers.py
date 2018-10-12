from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework import serializers

from listrik.models import Operator, Product, Transaction, ResponseTrx

# class OperatorListSerializer(ModelSerializer):
#     class Meta:
#         model = Operator
#         fields = [
#             'id', 'operator'
#         ]

# class OperatorDetailSerializer(ModelSerializer):
#     class Meta:
#         model = Operator
#         fields = [
#             'id', 'parse',
#             'operator',
#             'is_active'
#         ]

class ProductListSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id', 'nominal', 'price',
            'title', 'product_name', 'product_code'
        ]

class ProductDetailSerializer(ModelSerializer):
    description = SerializerMethodField()
    addinfo = SerializerMethodField()
    class Meta:
        model = Product
        fields = [
            'id', 'nominal', 'price',
            'title', 'product_name', 'product_code', 'description', 'addinfo'
        ]

    def get_description(self, instance):
        return instance.product_desc()

    def get_addinfo(self, instance):
        return instance.add_info()

# class TransactionSerializer(ModelSerializer):
#     class Meta:
#         model = Transaction
#         fields = [
#             'phone',
#             'product',
#         ]

class TransactionPostSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            'id',
            'trx_code', 'phone', 'product',
            'timestamp', 'closed'
        ]

    def validate_phone(self, value):
        try:
            d = int(value)
            return value
        except:
            raise serializers.ValidationError('Invalid phone number')


class TransactionDetailSerializer(ModelSerializer):
    detail_res = SerializerMethodField()
    class Meta:
        model = Transaction
        fields = [
            'id', 'detail_res'
        ]

    def get_detail_res(self, instance):
        return instance.get_detail_response()