from django.urls import path

from . import views

app_name = 'sale'
urlpatterns = [
    path('data/sale-chart-day/', views.chart_data_sale, name='sale_chart'),
    path('data/pulsa-chart/', views.chart_pulsa, name='pulsa_chart'),
    path('sale-list/', views.saleListView, name='sale_list'),
    path('profit/', views.saleProfitView, name='profit'),
    path('add-cash/', views.addCashSaldo, name='add_cash'),
    path('cash/', views.cashListView, name="cash_list"),
    path('cash/<int:id>/validation/', views.cashValidationView, name="cash_validation"),
    path('payment/', views.paymentListView, name='payment_list'),
    path('profit/bulk-update/', views.bulkProfitView, name='profit_bulk'),
]