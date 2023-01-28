import logging

import stripe
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from djstripe.models import Subscription, Price
from djstripe.utils import CURRENCY_SIGILS
from djstripe.settings import djstripe_settings

from stripe.api_resources.billing_portal.session import Session as BillingPortalSession
from stripe.api_resources.checkout import Session as CheckoutSession
from stripe.error import InvalidRequestError

from .exceptions import SubscriptionConfigError
from apps.users.models import CustomUser
from apps.web.meta import absolute_url


log = logging.getLogger("starter_app.subscription")


def get_friendly_currency_amount(price: Price):
    # modified from djstripe's version to only include sigil or currency, but not both
    if price.unit_amount_decimal is None:
        return 'Unknown'
    return get_price_display_with_currency(price.unit_amount_decimal / 100, price.currency)


def get_price_display_with_currency(amount: float, currency: str) -> str:
    currency = currency.upper()
    sigil = CURRENCY_SIGILS.get(currency, "")
    if sigil:
        return "{sigil}{amount:.2f}".format(sigil=sigil, amount=amount)
    else:
        return "{amount:.2f} {currency}".format(amount=amount, currency=currency)


def get_subscription_urls(subscription_holder):
    # get URLs for subscription helpers
    url_bases = [
        'subscription_details',
        'create_stripe_portal_session',
        'subscription_demo',
        'subscription_gated_page',
        'metered_billing_demo',

        # checkout urls
        'create_checkout_session',
        'checkout_success',
        'checkout_canceled',
    ]

    def _construct_url(base):
        return reverse(f'subscriptions:{base}')

    return {
        url_base: _construct_url(url_base) for url_base in url_bases
    }


def get_payment_metadata_from_request(request):
    return {
        'user_id': request.user.id,
        'user_email': request.user.email,
    }


def get_stripe_module():
    """Gets the Stripe API module, with the API key properly populated"""
    stripe.api_key = djstripe_settings.STRIPE_SECRET_KEY
    return stripe


def create_stripe_checkout_session(subscription_holder: CustomUser, stripe_price_id: str, user: CustomUser) -> CheckoutSession:
    stripe = get_stripe_module()

    success_url = absolute_url(reverse('subscriptions:checkout_success'))
    cancel_url = absolute_url(reverse('subscriptions:checkout_canceled'))

    customer_kwargs = {}
    if subscription_holder.customer:
        customer_kwargs['customer'] = subscription_holder.customer.id
    else:
        customer_kwargs['customer_email'] = user.email

    checkout_session = stripe.checkout.Session.create(
        success_url=success_url + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=cancel_url,
        payment_method_types=['card'],
        mode='subscription',
        client_reference_id=subscription_holder.id,
        line_items=[{
            'price': stripe_price_id,
            'quantity': _get_quantity(stripe_price_id, subscription_holder),
        }],
        allow_promotion_codes=True,
        subscription_data={
            'description': str(subscription_holder),
            'metadata': get_checkout_metadata(user),
        },
        **customer_kwargs,
    )
    return checkout_session


def get_checkout_metadata(user: CustomUser) -> dict:
    return {
        f"{djstripe_settings.SUBSCRIBER_CUSTOMER_KEY}": user.id,
        'user_id': user.id,
        'user_email': user.email,
        'user_name': user.get_full_name(),
    }


def _get_quantity(stripe_price_id, subscription_holder):
    """
    Get quantity for a given Stripe price and subscription holder
    """
    price = Price.objects.get(id=stripe_price_id)
    # if it's metered billing we shouldn't pass a quantity
    if price.recurring.get('usage_type', None) == 'metered':
        return None
    # otherwise we pass it from the subscription holder
    return subscription_holder.get_quantity()


def create_stripe_portal_session(subscription_holder: CustomUser) -> BillingPortalSession:
    stripe = get_stripe_module()
    if not subscription_holder.subscription or not subscription_holder.subscription.customer:
        raise SubscriptionConfigError(_("Whoops, we couldn't find a subscription associated with your account!"))

    subscription_urls = get_subscription_urls(subscription_holder)
    portal_session = stripe.billing_portal.Session.create(
        customer=subscription_holder.subscription.customer.id,
        return_url=absolute_url(subscription_urls['subscription_details']),
    )
    return portal_session


def provision_subscription(subscription_holder: CustomUser, subscription_id: str) -> Subscription:
    stripe = get_stripe_module()
    subscription = stripe.Subscription.retrieve(subscription_id)
    djstripe_subscription = Subscription.sync_from_stripe_data(subscription)
    subscription_holder.subscription = djstripe_subscription
    subscription_holder.save()
    return djstripe_subscription


def cancel_subscription(subscription_id: str):
    try:
        subscription = get_stripe_module().Subscription.delete(subscription_id)
    except InvalidRequestError as e:
        if e.code != 'resource_missing':
            log.error("Error deleting Stripe subscription: %s", e.user_message)
    else:
        Subscription.sync_from_stripe_data(subscription)
