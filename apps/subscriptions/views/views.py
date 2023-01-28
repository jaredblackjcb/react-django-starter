import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from djstripe.enums import PlanInterval, SubscriptionStatus
from djstripe.settings import djstripe_settings
from stripe.error import InvalidRequestError

from ..decorators import redirect_subscription_errors, active_subscription_required
from ..wrappers import SubscriptionWrapper, InvoiceFacade
from ..forms import UsageRecordForm
from ..helpers import (get_subscription_urls, get_payment_metadata_from_request,
    get_stripe_module)
from ..metadata import get_active_products_with_metadata, ACTIVE_PLAN_INTERVALS, get_active_plan_interval_metadata
from ..models import SubscriptionModelBase


log = logging.getLogger("starter_app.subscription")\


@redirect_subscription_errors
@login_required
def subscription(request):
    subscription_holder = request.user
    if subscription_holder.has_active_subscription():
        return _view_subscription(request, subscription_holder)
    else:
        return _upgrade_subscription(request, subscription_holder)


def _view_subscription(request, subscription_holder: SubscriptionModelBase):
    """
    Show user's active subscription
    """
    assert subscription_holder.has_active_subscription()
    subscription = subscription_holder.active_stripe_subscription
    wrapped_subscription = SubscriptionWrapper(subscription)
    next_invoice = None
    if not subscription.cancel_at_period_end:
        stripe = get_stripe_module()
        try:
            next_invoice = stripe.Invoice.upcoming(
                subscription=subscription.id,
            )
        except InvalidRequestError:
            # this error is raised if you try to get an invoice but the subcription is canceled
            # check if this happened and redirect to the upgrade page if so
            stripe_subscription = stripe.Subscription.retrieve(subscription.id)
            if stripe_subscription.status != SubscriptionStatus.active:
                log.warning('A canceled subscription was not synced to your app DB. '
                            'Your webhooks may not be set up properly. '
                            'See: https://docs.saaspegasus.com/subscriptions.html#webhooks')
                # update the subscription in the database and clear from the subscriptoin_holder
                subscription.sync_from_stripe_data(stripe_subscription)
                subscription_holder.refresh_from_db()
                subscription_holder.clear_cached_subscription()
                return _upgrade_subscription(request, subscription_holder)
            else:
                # failed for some other unexpected reason.
                raise

    return render(request, 'subscriptions/view_subscription.html', {
        'active_tab': 'subscription',
        'page_title': _('Subscription'),
        'subscription': wrapped_subscription,
        'next_invoice': InvoiceFacade(next_invoice) if next_invoice else None,
        'subscription_urls': get_subscription_urls(subscription_holder),
    })


def _upgrade_subscription(request, subscription_holder):
    """
    Show subscription upgrade form / options.
    """
    assert not subscription_holder.has_active_subscription()

    active_products = list(get_active_products_with_metadata())
    default_products = [p for p in active_products if p.metadata.is_default]
    default_product = default_products[0] if default_products else active_products[0]

    def _to_dict(product_with_metadata):
        # for now, just serialize the minimum amount of data needed for the front-end
        product_data = {}
        if PlanInterval.year in ACTIVE_PLAN_INTERVALS:
            product_data['annual_price'] = {
                'stripe_id': product_with_metadata.annual_price.id,
                'payment_amount': product_with_metadata.get_annual_price_display(),
                'interval': PlanInterval.year,
            }
        if PlanInterval.month in ACTIVE_PLAN_INTERVALS:
            product_data['monthly_price'] = {
                'stripe_id': product_with_metadata.monthly_price.id,
                'payment_amount': product_with_metadata.get_monthly_price_display(),
                'interval': PlanInterval.month,
            }
        return product_data

    template_name = 'subscriptions/upgrade_subscription.html'

    return render(request, template_name, {
        'active_tab': 'subscription',
        'stripe_api_key': djstripe_settings.STRIPE_PUBLIC_KEY,
        'default_product': default_product,
        'active_products': active_products,
        'active_products_json': {str(p.stripe_id): _to_dict(p) for p in active_products},
        'active_plan_intervals': get_active_plan_interval_metadata(),
        'default_to_annual': ACTIVE_PLAN_INTERVALS[0] == PlanInterval.year,
        'subscription_urls': get_subscription_urls(subscription_holder),
        'payment_metadata': get_payment_metadata_from_request(request),
    })


@login_required
def subscription_demo(request):
    subscription_holder = request.user
    subscription = subscription_holder.active_stripe_subscription
    wrapped_subscription = SubscriptionWrapper(subscription) if subscription else None
    return render(request, 'subscriptions/demo.html', {
        'active_tab': 'subscription_demo',
        'subscription': wrapped_subscription,
        'subscription_urls': get_subscription_urls(subscription_holder),
        'page_title': _('Subscription Demo'),
    })


@login_required
@active_subscription_required
def subscription_gated_page(request):
    return render(request, 'subscriptions/subscription_gated_page.html')


@login_required
@active_subscription_required
def metered_billing_demo(request):
    subscription_holder = request.user
    if request.method == 'POST':
        form = UsageRecordForm(subscription_holder, request.POST)
        if form.is_valid():
            usage_data = form.save()
            messages.info(request, _('Successfully recorded {} units for metered billing.').format(usage_data.quantity))
            return HttpResponseRedirect(reverse('subscriptions:subscription_demo'))
    else:
        form = UsageRecordForm(subscription_holder)

    if not form.is_usable():
        messages.info(request, _("It looks like you don't have any metered subscriptions set up. "
                                 "Sign up for a subscription with metered usage to use this UI."))
    return render(request, 'subscriptions/metered_billing_demo.html', {
        'subscription': subscription_holder.active_stripe_subscription,
        'form': form,
    })
