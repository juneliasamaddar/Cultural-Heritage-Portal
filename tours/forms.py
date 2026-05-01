from django import forms
from .models import Content
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ['title', 'description', 'location', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }
class SignupForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']