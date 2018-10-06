from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .resources import ProductResource, OperatorResource, ServerResource


# Register your models here.
from .models import (
    Operator,
    PrefixNumber, Product, Server, StatusTransaction, Transaction,
    ResponseTrx,
)

from .forms import OperatorForm, ServerForm, ProductForm

def activateProduct(modeladmin, request, queryset):
    queryset.update(is_active=True)

def inactiveProduct(modeladmin, request, queryset):
    queryset.update(is_active=False)

activateProduct.short_description = 'Activate selected Product'
inactiveProduct.short_description = 'Inactivate selected Product'


class PrefixNumberInline(admin.TabularInline):
    model = PrefixNumber
    extra = 1


@admin.register(Server)
class ServerAdmin(ImportExportModelAdmin):
    form = ServerForm
    resource_class = ServerResource


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    list_display = [
        'product_code' ,'operator', 'product_name', 'nominal', 'server', 'price', 'is_active'
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
    resource_class = ProductResource
    actions = [activateProduct, inactiveProduct]


@admin.register(Operator)
class OperatorAdmin(ImportExportModelAdmin):
    inlines = [PrefixNumberInline]
    form = OperatorForm
    resource_class = OperatorResource


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        'trx_code', 'product', 'price', 'get_responsetrx', 'record',
        'buyer', 'get_trx_status', 'timestamp'
    ]

admin.site.register(StatusTransaction)
admin.site.register(ResponseTrx)

