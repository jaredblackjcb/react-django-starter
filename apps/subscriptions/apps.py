from django.apps import AppConfig


class SubscriptionConfig(AppConfig):
    name = 'apps.subscriptions'
    label = 'subscriptions'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        from . import webhooks
        from . import signals
