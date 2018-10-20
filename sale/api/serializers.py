from rest_framework import serializers

from sale.models import Payment
from core.models import User

class UserTelegramDetailSerialiser(serializers.ModelSerializer):
    telegram = serializers.CharField(source='get_telegram', read_only=True)
    class Meta:
        model = User
        fields = [
            'id', 'telegram', 'first_name', 'saldo'
        ]

class PaymentSerializerList(serializers.ModelSerializer):
    user = UserTelegramDetailSerialiser(many=False, read_only=True)
    class Meta:
        model = Payment
        fields = [
            'id', 'nominal', 'timestamp',
            'user',
        ]

class PaymentSerializerNote(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'noted'
        ]