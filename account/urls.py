from django.urls import path

from . import views

app_name = 'account'
urlpatterns = [
    path('', views.indexView, name='index'),
    path('cart/', views.cartVIew, name="cart"),
    path('products/', views.productView, name='product'),
    path('sales/', views.saleView, name='sale'), 
    path('members/', views.memberView, name='member'),
    path('payment/', views.paymentView, name='payment'),
]