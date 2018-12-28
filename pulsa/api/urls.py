from django.urls import path

from . import views

app_name = 'api-pulsa'
urlpatterns = [
    path('prefix/', views.PrefixNumberListAPIView.as_view(), name='prefix_list'),
    path('operator/', views.OperatorListView.as_view(), name='operator_list'),
    path('operator_v2/', views.Operator_NoaListAPIView.as_view(), name='operator_list2'),
    path('operator/<int:pk>/', views.OperatorDetailView.as_view(), name='operator_detail'),
    path('product/', views.ProductListView.as_view(), name='product_list'),
    path('product_v2/', views.Product_NoaListAPIView.as_view(), name='product_list2'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('product_v2/<int:pk>/', views.Product_NoaDetailView.as_view(), name='product_detail2'),
    path('topup_v2/', views.TransactionCreateView.as_view(), name='topup2'),
    path('topup/', views.TransactionCreatePost.as_view(), name='topup'),
    path('trx/', views.TransactionListApiView.as_view(), name='transaction'),
    path('trx/tele/<int:pk>/', views.TeleTrxStatusRetryView.as_view(), name='trx_tele'),
    path('topup_v3/', views.TopupApiView.as_view(), name='topup3'),
    path('dev/topup/', views.TopupDevApiView.as_view(), name='dev_topup'),
]