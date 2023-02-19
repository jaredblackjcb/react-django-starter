from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# from apps.subscriptions.metadata import get_active_products_with_metadata
from apps.subscriptions.helpers import create_stripe_checkout_session

def home(request):
    if request.user.is_authenticated:
        if not request.user.has_active_subscription():
            if request.session['price_id']:
                # matched_products = [
                    # p for p in get_active_products_with_metadata() if p.stripe_id == request.session['price_id']
                # ]
                # if len(matched_products) == 1:
                    # matched_product = matched_products[0]
                    # stripe_id = matched_product.stripe_id
                    # price_id = request.s
                    checkout_session = create_stripe_checkout_session(request.user, request.session['price_id'], request.user)
                    request.session.clear()
                    return HttpResponseRedirect(checkout_session.url)
        return render(request, 'frontend/react_app.html')
    else:
        return render(request, 'web/landing_page.html')


def simulate_error(request):
    raise Exception('This is a simulated error.')
