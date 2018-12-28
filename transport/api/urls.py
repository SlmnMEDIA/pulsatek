from django.urls import path

from . import views

app_name = 'api-transport'
urlpatterns = [
    path('operator/', views.OperatorListView.as_view(), name='operator_list'),
    path('operator_v2/', views.OperatorNoAListView.as_view(), name='operator_list2'),
    path('operator/<int:pk>/', views.OperatorDetailView.as_view(), name='operator_detail'),
    path('product/', views.ProductListView.as_view(), name='product_list'),
    path('product_v2/', views.ProductNoAListView.as_view(), name='product_list2'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('product_v2/<int:pk>/', views.ProductNoADetailView.as_view(), name='product_detail2'),
    path('topup_v2/', views.TransactionCreateView.as_view(), name='topup2'),
    path('topup/', views.TransactionCreatePost.as_view(), name='topup'),
    path('trx/', views.TransactionListApiView.as_view(), name='transaction'),
    path('trx/tele/<int:pk>/', views.TeleTrxStatusRetryView.as_view(), name='trx_tele'),
    path('trx/goon/', views.TransactionGoProcess.as_view(), name='trx_goon'),
    path('topup_v3/', views.TopupApiView.as_view(), name='topup3'),
]