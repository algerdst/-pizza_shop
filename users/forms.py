import uuid
from datetime import timedelta

from django import forms
from django.contrib.auth.forms import (AuthenticationForm, UserChangeForm,
                                       UserCreationForm)
from django.utils.timezone import now

from users.models import EmailVerification, User


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form_control', 'placeholder': 'Логин'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form_control', 'placeholder': 'Пароль'}))

    class Meta:
        model = User
        fields = ['username', 'password']


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form_control', 'placeholder': 'Введите e-mail'}))
    image = forms.ImageField(required=False)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form_control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form_control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form_control'}))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form_control', 'placeholder': 'Введите пароль'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form_control', 'placeholder': 'Повторите пароль'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2', 'email', 'image']

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=True)
        expiration = now() + timedelta(hours=48)
        record = EmailVerification.objects.create(user=user, code=uuid.uuid4(), expiration=expiration)
        record.send_verification_email()
        return user


class UserProfileForm(UserChangeForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'name1', 'readonly': True}))
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'change_image'}))
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'name'}))
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'name'}))
    username = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'name1', 'readonly': True}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'image', 'password']
