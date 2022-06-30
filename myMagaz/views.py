from django.shortcuts import render
from django.views.generic import ListView, CreateView, View
from django.contrib.auth.views import LoginView, LogoutView
from .models import Product, MyUser, Purchase
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import MyUserCreationForm, AddProduct, PurchaseForm


class AdminIsLoginMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class Main(ListView):
    template_name = 'magaz-main.html'
    queryset = Product.objects.all()
    allow_empty = True
    ordering = None


class Registration(CreateView):
    model = MyUser
    template_name = 'registration.html'
    form_class = MyUserCreationForm
    success_url = 'magaz-main'


class LoginPage(LoginView):
    template_name = 'login.html'


class Logout(LoginRequiredMixin, LogoutView):
    next_page = '/magaz-main'


class AddProduct(AdminIsLoginMixin, CreateView):
    model = Product
    template_name = 'add_product.html'
    form_class = AddProduct
    success_url = 'add-product'


class PurchaseProduct(CreateView):
    model = Purchase
    success_url = 'magaz-main'
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        product = Product.objects.get(id=self.request.POST['product_id'])
        Purchase(client=self.request.user, product=product,
                 amount=self.request.POST['amount']).save()
        return super().form_valid()