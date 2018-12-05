from django.urls import path

from . import views

app_name = 'api-core'
urlpatterns = [
    path('get-token/', views.tokenKeyView, name='get-token'),
    path('telegram/create/', views.telegramRegisterPost, name='telegram-create'),
    path('site/<int:pk>/', views.SiteDetailView.as_view(), name='site_status'),
    path('message/', views.MessagePostListApiView.as_view(), name='message_list'),
    path('message/<int:pk>/', views.MessageApiUpdateView.as_view(), name='message_update'),
    path('telegram/<slug:telegram>/', views.TeleUserRetriaveApiView.as_view(), name='teleuser'),
]