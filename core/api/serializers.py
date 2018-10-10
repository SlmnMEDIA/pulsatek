from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers

from core.models import User, Telegram, StatusTransaction, SiteMaster, MessagePost
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


class SiteSerializer(ModelSerializer):
    class Meta:
        model = SiteMaster
        fields = [
            'status'
        ]

class UserResSerializer(ModelSerializer):
    teleid = serializers.CharField(source='get_telegram', read_only=True)
    class Meta:
        model = User
        fields = ['id', 'teleid']


class MessagePostSerializer(ModelSerializer):
    send_to = UserResSerializer(many=True, read_only=True)
    class Meta:
        model = MessagePost
        fields = [
            'id', 'subject', 'message', 'schedule',
            'send_to', 'sent_message_now', 'timestamp' 
        ]


class MessageUpdateSerializer(ModelSerializer):
    class Meta:
        model = MessagePost
        fields = [
            'closed'
        ]