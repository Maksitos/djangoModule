from django.shortcuts import render
from django.views.generic import ListView, CreateView, View
from django.contrib.auth.views import LoginView, LogoutView
from .models import Product, MyUser, Purchase
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import MyUserCreationForm, AddProduct
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic.edit import UpdateView
from django.db import transaction




class AdminIsLoginMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class Main(ListView):
    template_name = 'magaz-main.html'
    queryset = Product.objects.all().order_by('title')
    allow_empty = True

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


class PurchaseProduct(View):
    http_method_names = ['post']

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        product = Product.objects.get(id=self.request.POST['product_id'])
        total_cost = product.price * int(self.request.POST['amount'])
        user = request.user
        if total_cost > user.wallet:
            messages.add_message(request, messages.INFO, 'Недостаточно средств.')
        elif product.amount < int(self.request.POST['amount']):
            messages.add_message(request,messages.INFO, 'На складе не хватает товара для подобной покупки.')
        else:
            Purchase(client=user, product=product,
                 amount=self.request.POST['amount']).save()
            wallet_sum = user.wallet - total_cost
            new_amount = product.amount - int(self.request.POST['amount'])
            MyUser.objects.filter(username=user.username).update(wallet=wallet_sum)
            messages.add_message(request,messages.INFO, 'Успешная покупка')
            Product.objects.filter(id=product.id).update(amount=new_amount)
        return HttpResponseRedirect('magaz-main')


class UpdateProduct(UpdateView):
    model = Product
    fields = '__all__'
    success_url = '/magaz-main'
    template_name = 'add_product.html'


class MyPurchase(LoginRequiredMixin, ListView):
    template_name = 'my_purchase.html'
    allow_empty = True
    ordering = None

    def get(self, request, *args, **kwargs):
        self.queryset = Purchase.objects.filter(client=request.user)
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        if not allow_empty:
            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(_('Empty list and “%(class_name)s.allow_empty” is False.') % {
                    'class_name': self.__class__.__name__,
                })
        context = self.get_context_data()
        return self.render_to_response(context)

