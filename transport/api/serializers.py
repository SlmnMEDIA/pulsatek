from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework import serializers
from transport.models import Operator, Product, Transaction

from core.api.serializers import UserSaldoSerializer

from core.models import User
from datetime import date

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


# NEW
class TopupSerializer(serializers.Serializer):
    phone = serializers.CharField(write_only=True)
    product_code = serializers.CharField(write_only=True)

    def validate(self, data):
        product_code = data.get('product_code')
        prod_exists = Product.objects.filter(
            product_code=product_code, is_active=True
        ).exists()

        if not prod_exists:
            raise serializers.ValidationError({
                'product_code': 'Product not found'
            })
        
        return data


class TransactionNewSerializer(TopupSerializer, ModelSerializer):
    product = ProductDetailSerializer(read_only=True)
    buyer = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    status = SerializerMethodField()

    class Meta:
        model = Transaction
        fields = [
            'id',
            'trx_code', 'product',
            'timestamp', 'closed', 'buyer',
            't_notive', 'status', 'product_code', 'phone'
        ]

        read_only_fields = [
            'id',
            'trx_code', 'product',
            'timestamp', 'closed',
            't_notive', 'status'
        ]

    def get_status(self, obj):
        return obj.get_trx_status().status


    def validate(self, data):
        super().validate(data)

        buyer = data.get('buyer')
        product_code = data.get('product_code')
        phone = data.get('phone')

        product_obj = Product.objects.get(product_code=product_code)
        if buyer.saldo + buyer.limit < product_obj.price:
            raise serializers.ValidationError({
                'buyer': 'Saldo user tidak mencukupi'
            })

        double_trx = Transaction.objects.filter(
            product=product_obj, phone=phone, 
            timestamp__date=date.today(), record__success=True, record__debit=0
        ).exists()
        if double_trx:
            raise serializers.ValidationError({
                'phone': 'Doubel transaksi, silahkan pilih nominal lain'
            })

        return data


    def create(self, validated_data):
        phone = validated_data.get('phone')
        product_code = validated_data.get('product_code')

        product_obj = Product.objects.get(product_code=product_code)

        transaction_obj = Transaction.objects.create(
            product = product_obj,
            phone = phone,
            buyer = validated_data.get('buyer')
        )

        return transaction_obj