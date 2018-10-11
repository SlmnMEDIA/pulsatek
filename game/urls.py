from django.urls import path

from . import views

app_name = 'game'
urlpatterns = [
    path('product/', views.productListView, name='product_list'),
    path('topup/', views.newTrxview, name="topup"),
    path('bulk-update/', views.bulk_updateTransaction, name='update_bulk'),
]