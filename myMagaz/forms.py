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


class PurchaseForm(ModelForm):
    class Meta:
        model = Purchase
        fields = ['amount', 'client', 'product']



    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get('amount')
        client = cleaned_data.get('client')
        product = cleaned_data.get('product')
        TotalCost = product.price * amount
