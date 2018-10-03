from django.urls import path

from . import views

app_name = 'api-core'
urlpatterns = [
    path('get-token/', views.tokenKeyView, name='get-token'),
    path('telegram/create/', views.telegramRegisterPost, name='telegram-create'),
]