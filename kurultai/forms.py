from django import forms
from django.contrib.auth.forms import UserCreationForm
from kurultai.models import Account, Rubrics, Comment


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField

    class Meta:
        model = Account
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'birth_of_date']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_of_date': forms.TextInput(attrs={'class': 'form-control'}),
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
