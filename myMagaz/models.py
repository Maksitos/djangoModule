from django.db import models
from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    wallet = models.FloatField(default=10000, null=True, blank=True)


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1200)
    price = models.FloatField()
    amount = models.IntegerField()
    image = models.ImageField(upload_to='images', null=True, blank=True)


class Purchase(models.Model):
    client = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    time = models.TimeField(auto_now=True)
    amount = models.IntegerField()


class PurchaseReturn(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    time = models.TimeField(auto_now=True)

