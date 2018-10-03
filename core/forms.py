from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = [
            'email', 'first_name', 'last_name',
        ]

class LimitUserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = [
            'limit'
        ]

    def __init__(self, user, *args, **kwargs):
        super(LimitUserForm, self).__init__(*args, **kwargs)
        self.user_obj = user

    def clean_limit(self):
        limit = self.cleaned_data['limit']
        if not self.user_obj.is_superuser:
            if limit > self.user_obj.limit_max():
                raise forms.ValidationError('Error melebihi batas limit.')
        return limit
