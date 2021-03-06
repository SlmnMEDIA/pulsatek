from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from django.utils import timezone

from .models import Invitation, MessagePost, User

class AddUserFrom(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = [
            'email', 'first_name', 'last_name', 'password1', 'password2'
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email.lower()

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name is None or first_name == '':
            raise forms.ValidationError('User must be has a name.')
        return first_name.lower()

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        return last_name.lower()
        

class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = [
            'email', 'first_name', 'last_name', 'password1', 'password2'
        ]

    def __init__(self, ref=None, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        try :
            invit_obj = Invitation.objects.get(code=ref, closed=False)
            self.mail = invit_obj.email
        except:
            self.mail = None

    def clean_email(self):
        email = self.cleaned_data['email']
        if self.mail:
            if self.mail != email:
                raise forms.ValidationError('Invalid email invitations.')

        return email


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


class InvitationForm(forms.ModelForm):
    class Meta:
        model = Invitation
        fields = ['email']


    def clean_email(self):
        email = self.cleaned_data['email']
        if email is None or email == '':
            raise forms.ValidationError('Email cannot be empty.')

        user_class = get_user_model()
        user_exists = user_class.objects.filter(email=email).exists()
        if user_exists:
            raise forms.ValidationError('Email has been register. Cannot invite registered email.')

        return email


class MessagePostForm(forms.ModelForm):
    class Meta:
        model = MessagePost
        fields = [
            'send_to',
            'subject', 'message',
            'schedule',
        ]

    def __init__(self, user, *args, **kwargs):
        super(MessagePostForm, self).__init__(*args, **kwargs)
        self.fields['send_to'].queryset = User.objects.filter(telegram__isnull=False)
        if not user.is_superuser:
            if user.is_agen:
                self.fields['send_to'].queryset = User.objects.filter(leader=user, telegram__isnull=False)
        
    def clean_schedule(self):
        schedule = self.cleaned_data.get('schedule')
        if schedule is None or schedule == '':
            schedule = timezone.now()
        return schedule