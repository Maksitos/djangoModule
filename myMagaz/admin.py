from django.contrib import admin
from .models import MyUser, Product
# Register your models here.

admin.site.register(MyUser)
admin.site.register(Product)

