from django.apps import AppConfig


class AgrosmartiotwebConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'agrosmartiotweb'

    def ready(self):
        import agrosmartiotweb.signals

