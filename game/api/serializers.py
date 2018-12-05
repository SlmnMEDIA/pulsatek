from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework import serializers

from game.models import Operator, Product, Transaction

from core.api.serializers import UserSaldoSerializer

class OperatorListSerializer(ModelSerializer):
    class Meta:
        model = Operator
        fields = [
            'id', 'operator'
        ]

class OperatorDetailSerializer(ModelSerializer):
    class Meta:
        model = Operator
        fields = [
            'id', 'parse',
            'operator',
            'is_active'
        ]

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

class TransactionSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            'phone',
            'product',
        ]

class TransactionResposneSerializer(ModelSerializer):
    product = ProductDetailSerializer(read_only=True)
    buyer = UserSaldoSerializer(read_only=True)
    status = SerializerMethodField()
    class Meta:
        model = Transaction
        fields = [
            'id',
            'trx_code', 'phone', 'product',
            'timestamp', 'closed', 'buyer',
            't_notive', 'status'
        ]

    def get_status(self, instance):
        return instance.get_trx_status().status

class TransactionPostSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            'trx_code', 'phone', 'product',
            'timestamp', 'closed'
        ]

    def validate_phone(self, value):
        try:
            d = int(value)
            return value
        except:
            raise serializers.ValidationError('Invalid phone number')


class TeleTrxStatusSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            't_notive'
        ]