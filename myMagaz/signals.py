from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from .models import Product


@receiver(post_delete, sender=Product)
def image_delete(sender, instance, **kwargs):
    instance.image.delete(False)


