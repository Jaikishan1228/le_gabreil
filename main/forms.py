from django import forms
from .models import *
from django.contrib.auth import authenticate


class CustomerForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Customer
        fields = ('name','phone_number','email','category','enrollment','password')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone Number'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'category': forms.TextInput(attrs={'placeholder': 'Student/Staff'}),
            'enrollment': forms.TextInput(attrs={'placeholder': 'Enrollment'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Password'})
        }

class LoginForm(forms.Form):
    username = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(max_length=200, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Invalid username or password")
        return self.cleaned_data