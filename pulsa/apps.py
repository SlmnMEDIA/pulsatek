from django.apps import AppConfig


class PulsaConfig(AppConfig):
    name = 'pulsa'

    def ready(self):
        from . import signals