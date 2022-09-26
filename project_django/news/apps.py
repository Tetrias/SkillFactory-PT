from django.apps import AppConfig


class DistributionAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    def ready(self):
        from . import signals
