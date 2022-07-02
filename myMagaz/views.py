from django.shortcuts import render
from django.views.generic import ListView, CreateView, View
from django.contrib.auth.views import LoginView, LogoutView
from .models import Product, MyUser, Purchase, PurchaseReturn
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import MyUserCreationForm, AddProduct
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic.edit import UpdateView
from django.db import transaction
from django.utils import timezone



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
            MyUser.objects.filter(id=user.id).update(wallet=wallet_sum)
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

    def get(self, request, *args, **kwargs):
        self.queryset = Purchase.objects.filter(client=request.user)
        return super().get(self, request, *args, **kwargs)


class PurchaseReturns(View):

    def post(self, request, *args, **kwargs):
        purchase = Purchase.objects.get(id=self.request.POST['purchase_id'])
        if (timezone.now() - purchase.time).seconds > 180:
            messages.add_message(request, messages.INFO, 'Прошло более трех минут')
        elif PurchaseReturn.objects.filter(purchase=purchase):
            messages.add_message(request, messages.INFO, 'Данная покупка ожидает решение администрации по поводу возврата.')
        else:
            PurchaseReturn(purchase=purchase).save()
        return HttpResponseRedirect('my-purchase')


class PurchaseReturnsList(AdminIsLoginMixin, ListView):
    template_name = 'purchase-return.html'
    queryset = PurchaseReturn.objects.all()


class PurchaseReturnsResult(View):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        purchase_return = PurchaseReturn.objects.get(id=self.request.POST['return_id'])
        purchase = Purchase.objects.get(id=purchase_return.purchase_id)
        client = MyUser.objects.get(id=purchase.client_id)
        if self.request.POST['action'] == 'approve':
            total_cost = purchase.amount * purchase.product.price
            wallet_sum = client.wallet + total_cost
            new_amount = purchase.amount + purchase.product.amount
            MyUser.objects.filter(id=client.id).update(wallet=wallet_sum)
            Product.objects.filter(id=purchase.product_id).update(amount=new_amount)
            purchase.delete()
        else:
            purchase_return.delete()
        return HttpResponseRedirect('purchase-returns-list')

