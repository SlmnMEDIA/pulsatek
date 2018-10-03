from django import forms

from .models import Transaction, Operator, Product

class NewTransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            'phone', 'product'
        ]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def clean_product_code(self):
        return self.cleaned_data.get('product_code').upper()

    def clean_product_name(self):
        return self.cleaned_data.get('product_name').upper()

    def clean_title(self):
        return self.cleaned_data.get('title').upper()


class OperatorFrom(forms.ModelForm):
    class Meta:
        model = Operator
        fields = ['operator', 'is_active']

    def clean_operator(self):
        return self.cleaned_data.get('operator').upper()