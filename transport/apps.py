from django.apps import AppConfig


class TransportConfig(AppConfig):
    name = 'transport'

    def ready(self):
        from . import signals