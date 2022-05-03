from .models import Order
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm 
from django import forms
from django.contrib.auth.models import User
import re
from django.core.exceptions import ObjectDoesNotExist 
class OrderForm (ModelForm):
    class Meta:
        model = Order 
        fields = '__all__'
class CreateUserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-input form-control'}))
    username = forms.CharField(label= 'Tài Khoản', widget=forms.TextInput(attrs={'class':'form-input form-control'}))
    password1 = forms.CharField(label= 'Mật Khẩu', widget=forms.PasswordInput(attrs={'class':'form-input form-control'}))
    password2 = forms.CharField(label= 'Nhập Lại Mật Khẩu', widget=forms.PasswordInput(attrs={'class':'form-input form-control'}))
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    # def clean_password(self):
    #     if self.data['password1'] != self.data['password2']:
    #         raise forms.ValidationError('Mật khẩu không giống nhau')
    #     return self.data['password']
    # def clean_username(self):
    #     username = self.cleaned_data['username']
    #     if not re.search(r'^/+$'):
    #         raise forms.ValidationError("Tên tài khỏan không được có kí tự đặc biệt")
    #     try:
    #         User.objects.get(username=username)
    #     except ObjectDoesNotExist:
    #         return username
    #     raise forms.ValidationError("Tên tài khoản đã tồn tại")
