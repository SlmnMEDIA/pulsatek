from django.contrib import admin

# Register your models here.
from .models import (
    Operator,
    PrefixNumber, Product, Server, StatusTransaction, Transaction,
    ResponseTrx,
)

from .forms import OperatorForm, ServerForm, ProductForm


class PrefixNumberInline(admin.TabularInline):
    model = PrefixNumber
    extra = 1


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    form = ServerForm


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'operator', 'product_name', 'nominal', 'price', 'is_active'
    ]
    list_display_links = [
        'operator', 'product_name'
    ]
    list_filter = [
        'is_active', 'product_type'
    ]
    search_fields = [
        'product_code', 'product_name'
    ]
    form = ProductForm


@admin.register(Operator)
class OperatorAdmin(admin.ModelAdmin):
    inlines = [PrefixNumberInline]
    form = OperatorForm


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        'trx_code', 'product', 'price', 'get_responsetrx', 'record',
        'buyer', 'get_trx_status', 'timestamp'
    ]

admin.site.register(StatusTransaction)
admin.site.register(ResponseTrx)

