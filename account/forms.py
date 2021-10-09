from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm,
                                       SetPasswordForm)

from account.models import ApplyAuthor, Institution

User = get_user_model()


class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(max_length=264, error_messages={
        'required': 'Sorry, you will need an email'})
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput)
    name = forms.CharField(max_length=264, error_messages={
        'required': "Please Enter your name"
    })

    class Meta:
        model = User
        fields = ('email', 'name', 'gender', 'country', 'image')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Please use another Email, that is already taken')
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Username', 'id': 'login-username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'id': 'login-pwd',
        }
    ))


class PwdResetForm(PasswordResetForm):

    email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'form-email'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        u = User.objects.filter(email=email)
        if not u:
            raise forms.ValidationError(
                'Unfortunatley we can not find that email address')
        return email


class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='New password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-newpass'}))
    new_password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-new-pass2'}))


class EditProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('name', 'headline', 'gender', 'birthday',
                  'country', 'description', 'image')


class InstitutionForm(forms.ModelForm):
    class Meta:
        model = Institution
        fields = ("name", "subject", "degree", "start_year",
                  "graduated", "end_year", "description")


class AuthorApplicationForm(forms.ModelForm):
    class Meta:
        model = ApplyAuthor
        fields = ("description",)