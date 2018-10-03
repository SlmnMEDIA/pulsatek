from django.urls import path

from . import views

app_name = 'transport'
urlpatterns = [
    path('product/', views.productListView, name='product_list'),
    path('topup/', views.newTrxview, name="topup"),
]