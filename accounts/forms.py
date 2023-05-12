from django import forms
from django.http import JsonResponse

from .models import *


class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=40, widget=forms.PasswordInput())
    password = forms.CharField(max_length=40, widget=forms.PasswordInput())

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("The two password fields didn't match.")


class UserForm(forms.ModelForm):

    class Meta:
        model = Account

        fields = ('first_name', 'last_name', 'phone_number')

    def __init__(self, *args, **kwargs):

        super(UserForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control ed_p-input'


class UserProfileForm(forms.ModelForm):

    profile_picture = forms.ImageField(required=False, error_messages={"Invalid": ("Image files only")}, widget=forms.FileInput)

    class Meta:
        model = UserProfile

        fields = ('address_line_1', 'address_line_2', 'country', 'city', 'profile_picture')

    def __init__(self, *args, **kwargs):

        super(UserProfileForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control ed_p-input'