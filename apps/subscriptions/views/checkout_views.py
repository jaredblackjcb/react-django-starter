from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_POST

from apps.subscriptions.helpers import (
    get_stripe_module, get_subscription_urls, create_stripe_checkout_session, provision_subscription
)
from apps.subscriptions.wrappers import SubscriptionWrapper


@require_POST
@login_required
def create_checkout_session(request):
    subscription_holder = request.user
    price_id = request.POST['priceId']
    checkout_session = create_stripe_checkout_session(subscription_holder, price_id, request.user)
    return HttpResponseRedirect(checkout_session.url)


@login_required
def checkout_success(request):
    subscription_holder = request.user
    session_id = request.GET.get('session_id')
    stripe = get_stripe_module()
    session = stripe.checkout.Session.retrieve(session_id)
    assert int(session.client_reference_id) == subscription_holder.id

    if not subscription_holder.subscription or subscription_holder.subscription.id != session.subscription:
        # provision subscription
        djstripe_subscription = provision_subscription(subscription_holder, session.subscription)
    else:
        # already provisioned (likely by webhook)
        djstripe_subscription = subscription_holder.subscription

    # set customer object if necessary
    if not subscription_holder.customer:
        subscription_holder.customer = djstripe_subscription.customer
        subscription_holder.save()

    subscription_name = SubscriptionWrapper(djstripe_subscription).display_name
    messages.success(request, f"You've successfully signed up for {subscription_name}. "
                              "Thanks for the support!")
    return HttpResponseRedirect(get_subscription_urls(subscription_holder)['subscription_details'])


@login_required
def checkout_canceled(request):
    subscription_holder = request.user
    messages.info(request, 'Your upgrade was canceled.')
    return HttpResponseRedirect(get_subscription_urls(subscription_holder)['subscription_details'])
