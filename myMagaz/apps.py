from django.apps import AppConfig


class MymagazConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myMagaz'

    def ready(self):
        from .signals import image_delete