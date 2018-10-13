from django import forms
from django.db.models import Q

from .models import (
    Product, Transaction, Operator, Server
)


class NewProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'operator', 'product_type', 'product_code',
            'server', 'title',
            'nominal', 'price',
        ]


class NewTransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            'phone', 'product'
        ]

    def __init__(self, user, *args, **kwargs):
        super(NewTransactionForm, self).__init__(*args, **kwargs)
        self.balance = user.saldo + user.limit

    def clean_product(self):
        prod = self.cleaned_data['product']
        if self.balance - prod.price < 0:
            raise forms.ValidationError('Saldo is not enough.')
        return prod


class OperatorForm(forms.ModelForm):
    class Meta:
        model = Operator
        fields = ['operator', 'is_active']

    def clean_operator(self):
        return self.cleaned_data.get('operator').upper()


class ServerForm(forms.ModelForm):
    class Meta:
        model = Server
        fields = '__all__'

    def clean_code(self):
        return self.cleaned_data.get('code').upper()

    def clean_product_name(self):
        return self.cleaned_data.get('product_name').upper()


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['server'].queryset = Server.objects.filter(Q(product__isnull=True) | Q(product__id = self.instance.id))
           
    def clean_product_code(self):
        return self.cleaned_data.get('product_code').upper()

    def clean_product_name(self):
        return self.cleaned_data.get('product_name').upper()
    
    def clean_title(self):
        return self.cleaned_data.get('title').upper()
