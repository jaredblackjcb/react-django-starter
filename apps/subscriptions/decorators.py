from typing import List

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .exceptions import SubscriptionConfigError
from .metadata import get_product_with_metadata


class redirect_subscription_errors(object):
    """
    Meant to be used with django views only.
    """
    def __init__(self, f):
        self.f = f

    def __call__(self, request, *args, **kwargs):
        try:
            return self.f(request, *args, **kwargs)
        except SubscriptionConfigError as e:
            return TemplateResponse(request, 'subscriptions/bad_config.html', {'error': str(e)}, status=500)


class _ActiveSubscriptionRequired:
    # decorator follows this pattern: https://stackoverflow.com/a/7492124/8207

    def __init__(self, f, limit_to_plans=None):
        self.f = f
        self.limit_to_plans = limit_to_plans or []

    def __call__(self, request, *args, **kwargs):
        proceed = False
        if not request.user.is_authenticated:
            return HttpResponseRedirect('{}?next={}'.format(reverse('account_login'), request.path))

        subscription_holder = request.user
        if not subscription_holder:
            proceed = False
        elif not subscription_holder.has_active_subscription():
            messages.info(request, _("Sorry, that page requires an active subscription. You've been redirected."))
            proceed = False
        elif self.limit_to_plans:
            subscription = subscription_holder.active_stripe_subscription
            for item in subscription.items.select_related('price__product'):
                product_metadata = get_product_with_metadata(item.price.product).metadata
                if product_metadata.slug in self.limit_to_plans:
                    proceed = True
                    break
            if not proceed:
                messages.info(request, _("Sorry, that page requires a higher subscription tier. "
                                         "Upgrade your plan to continue."))
        else:
            # had an active subscription and wasn't limited to plans
            proceed = True

        if proceed:
            return self.f(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('subscriptions:subscription_details'))


def active_subscription_required(function=None, limit_to_plans: List[str] = None):
    """
    Prevents accessing a view unless the user has an active subscription.
    You can optionally limit to a list of plans (by slug) which should allow access
    (default is any active subscription).
    """
    if function:
        return _ActiveSubscriptionRequired(function, limit_to_plans)
    else:
        def wrapper(function):
            return _ActiveSubscriptionRequired(function, limit_to_plans)

        return wrapper
