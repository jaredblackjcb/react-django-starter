from django.db import models
from django.db.models import F, Q
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from djstripe.enums import SubscriptionStatus
from djstripe.models import Customer

from apps.subscriptions.wrappers import SubscriptionWrapper


class SubscriptionModelBase(models.Model):
    """
    Helper class to be used with Stripe Subscriptions.

    Assumes that the associated subclass is a django model containing a
    subscription field that is a ForeignKey to a djstripe.Subscription object.
    """
    # subclass should override with appropriate foreign keys as needed
    subscription = models.ForeignKey('djstripe.Subscription', null=True, blank=True, on_delete=models.SET_NULL,
                                     help_text=_("The associated Stripe Subscription object, if it exists"))
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    billing_details_last_changed = models.DateTimeField(
        default=timezone.now,
        help_text=_(
            'Updated every time an event that might trigger billing happens.'
        )
    )
    last_synced_with_stripe = models.DateTimeField(null=True, blank=True,
                                                   help_text=_('Used for determining when to next sync with Stripe.'))

    class Meta:
        abstract = True

    @cached_property
    def active_stripe_subscription(self):
        if self.subscription and self.subscription.status == SubscriptionStatus.active:
            return self.subscription
        return None

    @cached_property
    def wrapped_subscription(self):
        """
        Returns the current subscription as a SubscriptionWrapper
        """
        if self.subscription:
            return SubscriptionWrapper(self.subscription)
        return None

    def clear_cached_subscription(self):
        """
        Clear the cached subscription object (in case it has changed since the model was created)
        """
        try:
            del self.active_stripe_subscription
        except AttributeError:
            pass
        try:
            del self.wrapped_subscription
        except AttributeError:
            pass

    def has_active_subscription(self) -> bool:
        return self.active_stripe_subscription is not None

    @classmethod
    def get_items_needing_sync(cls):
        return cls.objects.filter(
            Q(last_synced_with_stripe__isnull=True) | Q(last_synced_with_stripe__lt=F('billing_details_last_changed')),
            subscription__status=SubscriptionStatus.active,
        )

    def get_quantity(self) -> int:
        # if you use "per-seat" billing, override this accordingly
        return 1
