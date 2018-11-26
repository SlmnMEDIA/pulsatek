from django.urls import path

from . import views

app_name = 'api-pulsa'
urlpatterns = [
    path('prefix/', views.PrefixNumberListAPIView.as_view, name='prefix_list'),
    path('operator/', views.OperatorListView.as_view(), name='operator-list'),
    path('operator_v2/', views.Operator_NoaListAPIView.as_view(), name='operator_list2'),
    path('operator/<int:pk>/', views.OperatorDetailView.as_view(), name='operator-detail'),
    path('product/', views.ProductListView.as_view(), name='product-list'),
    path('product_v2/', views.Product_NoaListAPIView.as_view(), name='product_list2'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    # path('topup/', views.TransactionCreateView.as_view(), name='topup'),
    path('topup/', views.TransactionCreatePost.as_view(), name='topup'),
]