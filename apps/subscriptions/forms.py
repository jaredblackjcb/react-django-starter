from django import forms
from django.utils.translation import gettext_lazy as _

from apps.subscriptions.models import SubscriptionModelBase
from djstripe.models import SubscriptionItem, UsageRecord


class UsageRecordForm(forms.Form):
    """
    Form for recording usage of a metered subscription.
    """
    subscription_item = forms.ModelChoiceField(SubscriptionItem.objects.none(), label=_('Product'))
    quantity = forms.IntegerField(initial=1, min_value=1)

    def __init__(self, subscription_holder: SubscriptionModelBase, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # limit the subscription item choices to those matching the current subscription
        self.metered_plans = subscription_holder.active_stripe_subscription.items.filter(
            price__recurring__usage_type='metered',
        )
        self.fields['subscription_item'].queryset = self.metered_plans
        # display products in the dropdown
        self.fields['subscription_item'].label_from_instance = lambda item: item.price.product.name

    def is_usable(self):
        return self.metered_plans.exists()

    def save(self) -> UsageRecord:
        subscription_item = self.cleaned_data['subscription_item']
        quantity = self.cleaned_data['quantity']
        return UsageRecord.create(id=subscription_item.id, quantity=quantity)
