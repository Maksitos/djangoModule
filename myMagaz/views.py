from django.shortcuts import render
from django.views.generic import ListView
from .models import Product


class Main(ListView):
    template_name = 'magaz-main.html'
    queryset = Product.objects.all()
    allow_empty = True
    ordering = None