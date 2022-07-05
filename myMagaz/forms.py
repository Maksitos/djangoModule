from django.contrib.auth.forms import UserCreationForm
from .models import MyUser, Product, Purchase
from django.forms import ModelForm, HiddenInput


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ("username",)


class AddProduct(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

