from django.contrib import admin

# Register your models here.
from .models import (
    Operator, Product, Server, StatusTransaction, Transaction,
    ResponseTrx,
)

from .forms import ProductForm, ServerForm, OperatorForm

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'operator', 'product_name', 'nominal', 'price', 'is_active'
    ]
    list_display_links = [
        'operator', 'product_name'
    ]
    list_filter = [
        'is_active'
    ]
    search_fields = [
        'product_code', 'product_name'
    ]
    form = ProductForm

@admin.register(Operator)
class OperatorAdmin(admin.ModelAdmin):
    form = OperatorForm

@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    form = ServerForm


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        'trx_code', 'product', 'price', 'get_responsetrx', 'record',
        'buyer', 'get_trx_status', 'timestamp'
    ]

admin.site.register(StatusTransaction)
admin.site.register(ResponseTrx)

