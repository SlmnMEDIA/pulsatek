from django.apps import AppConfig


class ListrikConfig(AppConfig):
    name = 'listrik'

    def ready(self):
        from . import signals