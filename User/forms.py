from django import forms
from django.contrib.auth.models import User
from .models import *


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Username',
                               widget=forms.TextInput(attrs={'class': 'mdl-textfield__input', 'autocomplete': 'off'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'mdl-textfield__input'}))
    first_name = forms.CharField(label='First Name',
                                 widget=forms.TextInput(attrs={'class': 'mdl-textfield__input', 'autocomplete': 'off'}))
    last_name = forms.CharField(label='Last Name',
                               widget=forms.TextInput(attrs={'class': 'mdl-textfield__input', 'autocomplete': 'off'}))
    email = forms.CharField(label='Email',
                               widget=forms.EmailInput(attrs={'class': 'mdl-textfield__input', 'autocomplete': 'off'}))
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']


class LoginForm(forms.Form):
    username = forms.CharField(label='Username',
                               widget=forms.TextInput(attrs={'class': 'mdl-textfield__input', 'autocomplete': 'off'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'mdl-textfield__input'}))


class UploadCSVForm(forms.ModelForm):
    filename = forms.CharField(label='Filename',
                               widget=forms.TextInput(attrs={'class': 'mdl-textfield__input', 'autocomplete': 'off'}))
    class Meta:
        model = UploadedCSV
        fields = '__all__'


class ProductForm(forms.ModelForm):
    order_id = forms.CharField(label='Order Id',
                               widget=forms.TextInput(attrs={'class': 'mdl-textfield__input', 'autocomplete': 'off'}))
    # order_status = forms.ChoiceField(label='Order Status')
    product_code = forms.CharField(label='Product Code',
                                   widget=forms.TextInput(
                                       attrs={'class': 'mdl-textfield__input', 'autocomplete': 'off'}))
    product_name = forms.CharField(label='Product Name',
                                   widget=forms.TextInput(
                                       attrs={'class': 'mdl-textfield__input', 'autocomplete': 'off'}))
    product_url = forms.CharField(label='Product Url',
                                  widget=forms.TextInput(
                                      attrs={'class': 'mdl-textfield__input', 'autocomplete': 'off'}))
    cost_price = forms.FloatField(label='Cost Price',
                                  widget=forms.TextInput(
                                      attrs={'class': 'mdl-textfield__input', 'autocomplete': 'off'}))

    class Meta:
        model = Product
        fields = '__all__'
