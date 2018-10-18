from django import forms
from django.contrib.auth import get_user_model

from .models import Cash

userClass = get_user_model()

class AddCashForm(forms.ModelForm):
    class Meta:
        model = Cash
        fields = [
            'user', 'nominal'
        ]

    def __init__(self, user, *args, **kwargs):
        super(AddCashForm, self).__init__(*args, **kwargs)
        if not user.is_superuser:
            self.fields['user'].queryset = userClass.objects.filter(leader=user)