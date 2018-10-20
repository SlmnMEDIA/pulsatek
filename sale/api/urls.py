from django.urls import path

from . import views

app_name = 'api-sale'
urlpatterns = [
    path('payment/', views.PaymentAPIRetriList.as_view(), name='payment_list'),
    path('payment/<int:pk>/', views.PaymentNoteUpdateAPInote.as_view(), name='payment_noted'),
]