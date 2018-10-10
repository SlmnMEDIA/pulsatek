from rest_framework.views import APIView, View
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView, RetrieveAPIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

import pytz
from datetime import datetime


from core.models import User, SiteMaster, MessagePost
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view

from .serializers import (
    TokenSerializer, TelegramSerilizer, SiteSerializer, 
    MessagePostSerializer, MessageUpdateSerializer
)


@api_view(['POST'])
def tokenKeyView(request):
    try :
        token_obj = Token.objects.get(user__telegram__telegram=request.data['telegram'])
        serializer = TokenSerializer(token_obj)
        return Response(serializer.data)
    except:
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def telegramRegisterPost(request):
    user_obj = User.objects.filter(pin=request.data['pin'], telegram__isnull=True)
    if not user_obj.exists():
        return Response(status=status.HTTP_204_NO_CONTENT)

    data = {
        'telegram': request.data['telegram'],
        'user': user_obj.get().id
    }
    serializer = TelegramSerilizer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SiteDetailView(RetrieveAPIView):
    queryset = SiteMaster.objects.all()
    serializer_class = SiteSerializer



class MessagePostListApiView(ListAPIView):
    queryset = MessagePost.objects.filter(closed=False, schedule__lte=timezone.now())
    serializer_class = MessagePostSerializer
    # permission_classes = [
    #     IsAuthenticated
    # ]



class MessageApiUpdateView(RetrieveUpdateAPIView):
    queryset = MessagePost.objects.filter(closed=False)
    serializer_class = MessageUpdateSerializer
    # permission_classes = [
    #     IsAuthenticated
    # ]