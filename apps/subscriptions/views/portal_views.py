from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_POST

from apps.subscriptions.helpers import create_stripe_portal_session


@login_required
@require_POST
def create_portal_session(request, subscription_holder=None):
    subscription_holder = request.user
    portal_session = create_stripe_portal_session(subscription_holder)
    return HttpResponseRedirect(portal_session.url)
