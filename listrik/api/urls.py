from django.urls import path

from . import views

app_name = 'api-listrik'
urlpatterns = [
#     path('operator/', views.OperatorListView.as_view(), name='operator-list'),
#     path('operator/<int:pk>/', views.OperatorDetailView.as_view(), name='operator-detail'),
    path('product/', views.ProductListView.as_view(), name='product-list'),
    path('product_v2/', views.ProductNoAListView.as_view(), name='product-list2'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('product_v2/<int:pk>/', views.ProductNoADetailView.as_view(), name='product-details'),
    path('topup_v2/', views.TransactionCreateView.as_view(), name='topup2'),
    path('topup/', views.TransactionCreatePost.as_view(), name='topup'),
    path('trx/<int:pk>/', views.TransactionDetailSerApi.as_view(), name='trx_detail'),
    path('trx/', views.TransactionListApiView.as_view(), name='transaction'),
    path('trx/tele/<int:pk>/', views.TeleTrxStatusRetryView.as_view(), name='trx_tele'),
]