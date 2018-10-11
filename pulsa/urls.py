from django.urls import path

from . import views

app_name = 'pulsa'
urlpatterns = [
    path('product/', views.productListView, name='product_list'),
    path('product-data/', views.productDataList, name='product_data'),
    path('product/add/', views.addproductView, name='create'),
    path('topup/', views.newTrxview, name="topup"),
    path('bulk-update/', views.bulk_updateTransaction, name='update_bulk'),
]