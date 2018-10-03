from rest_framework.views import APIView, View
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework import status
from core.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view

from .serializers import TokenSerializer, TelegramSerilizer


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


