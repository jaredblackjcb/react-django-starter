from django.db.models.signals import post_delete
from django.dispatch import receiver

from apps.subscriptions.helpers import cancel_subscription
from apps.users.models import CustomUser



@receiver(post_delete, sender=CustomUser)
def cancel_subscription_on_user_delete(sender, instance: CustomUser, **kwargs):
    if instance.has_active_subscription():
        cancel_subscription(instance.subscription.id)
