from .models import Order
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm 
from django import forms
from django.contrib.auth.models import User
import re
from django.core.exceptions import ObjectDoesNotExist 
# class OrderForm (ModelForm):
#     class Meta:
#         model = Order 
#         fields = '__all__'

#hàm xử lý dữ liệu trong form đăng ký
class CreateUserForm(UserCreationForm):
    """class tạo form đăng ký"""
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-input form-control'}))
    username = forms.CharField(label= 'Tài Khoản', widget=forms.TextInput(attrs={'class':'form-input form-control'}))
    password1 = forms.CharField(label= 'Mật Khẩu', widget=forms.PasswordInput(attrs={'class':'form-input form-control'}))
    password2 = forms.CharField(label= 'Nhập Lại Mật Khẩu', widget=forms.PasswordInput(attrs={'class':'form-input form-control'}))
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_password2(self):
        """hàm kiểm tra password có trùng nhau không"""
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            raise forms.ValidationError('Mật khẩu không giống nhau')
        return self.data['password1']

    def clean_username(self):
        """hàm kiểm tra xem tên tài khoản có tồn tại không"""
        username = self.cleaned_data['username']
        
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError("Tên tài khoản đã tồn tại")
