from django.urls import path

from . import views

app_name = 'api-listrik'
urlpatterns = [
#     path('operator/', views.OperatorListView.as_view(), name='operator-list'),
#     path('operator/<int:pk>/', views.OperatorDetailView.as_view(), name='operator-detail'),
    path('product/', views.ProductListView.as_view(), name='product-list'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
#     # path('topup/', views.TransactionCreateView.as_view(), name='topup'),
    path('topup/', views.TransactionCreatePost.as_view(), name='topup'),
    path('trx/<int:pk>/', views.TransactionDetailSerApi.as_view(), name='trx_detail'),
]