from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField
    # birth_of_date = forms.DateField

    class Meta:
        model = Account
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            # 'birth_of_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),

        }


class RubricForm(forms.ModelForm):

    class Meta:
        model = Rubrics
        fields = '__all__'


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')


class Comment_mode_Form(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'preview']


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField

    class Meta:
        model = Account
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'birth_of_date']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_of_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),

        }
