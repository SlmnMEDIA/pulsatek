from django.apps import AppConfig


class SaleConfig(AppConfig):
    name = 'sale'


    def ready(self):
        from . import signals