from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone



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
    time = models.DateTimeField(default=timezone.now)
    amount = models.IntegerField()


class PurchaseReturn(models.Model):
    purchase = models.OneToOneField(Purchase, on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now)

