from django.contrib import admin

# Register your models here.

from .models import (
    Sale, Payment, Cash
)

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['trx_obj', 'type_income', 'debit', 'credit', 'balance', 'ref', 'user', 'timestamp']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    pass

@admin.register(Cash)
class CashAdmin(admin.ModelAdmin):
    pass