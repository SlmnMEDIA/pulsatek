from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers

from core.models import User, Telegram, StatusTransaction
from rest_framework.authtoken.models import Token

class TelegramSerilizer(ModelSerializer):
    class Meta:
        model = Telegram
        fields = ['user', 'telegram']

class TokenSerializer(ModelSerializer):
    class Meta:
        model = Token
        fields = ['key']


class StatusTransactionSrializer(ModelSerializer):
    class Meta:
        model = StatusTransaction
        fields = [
            'code', 'description'
        ]
