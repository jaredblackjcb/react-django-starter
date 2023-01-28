import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView

from apps.web.meta import absolute_url
from ..models import Payment

EXPECTED_PAYMENT_AMOUNT = 2500  # in cents


@method_decorator(login_required, name='dispatch')
class PaymentView(TemplateView):
    template_name = 'pegasus/examples/payments/payments.html'

    def get_context_data(self, **kwargs):
        return {
            'stripe_key': settings.STRIPE_TEST_PUBLIC_KEY,
            'payments': self.request.user.pegasus_payments.all(),
            'amount': EXPECTED_PAYMENT_AMOUNT,
            'active_tab': 'payments',
        }


@login_required
@require_POST
def create_payment_intent(request):
    stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
    intent = stripe.PaymentIntent.create(
        amount=EXPECTED_PAYMENT_AMOUNT,
        currency='usd',
        description=f'A Demo Payment',
    )
    return JsonResponse({
        'client_secret': intent['client_secret'],
    })


@login_required
def payment_confirm(request, payment_id):
    """
    Confirmation page after making a payment.
    """
    payment = get_object_or_404(Payment, user=request.user, id=payment_id)
    return render(request, 'pegasus/examples/payments/payment_confirm.html', {
        'payment': payment,
        'active_tab': 'payments',
    })


@login_required
@require_POST
def accept_payment(request):
    """
    Accept a payment with a token from Stripe
    """
    stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
    name = request.POST['name']
    try:
        payment_intent_id = request.POST['paymentIntent']
    except KeyError:
        messages.error(request, 'Problem processing that payment. Please try again!')
        return HttpResponseRedirect(reverse('pegasus_examples:payments'))
    payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
    if payment_intent.status != 'succeeded':
        raise Exception(f'Unexpected payment intent status: {payment_intent.status}')

    amount = payment_intent['amount']
    if amount != EXPECTED_PAYMENT_AMOUNT:
        raise ValueError(f'Unexpected payment amount {payment_intent["amount"]}')

    charge = payment_intent['charges']['data'][0]

    stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
    user = request.user
    payment = Payment.objects.create(
        charge_id=charge.id,
        amount=charge.amount,
        name=name,
        user=user,
    )
    return HttpResponseRedirect(reverse('pegasus_examples:payment_confirm', args=[payment.payment_id]))


@require_POST
@login_required
def create_checkout_session(request):
    stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
    success_url = absolute_url(reverse('pegasus_examples:checkout_success'))
    cancel_url = absolute_url(reverse('pegasus_examples:checkout_canceled'))
    checkout_session = stripe.checkout.Session.create(
        success_url=success_url + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=cancel_url,
        customer_email=request.user.email,
        payment_method_types=['card'],
        mode='payment',
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'Sample Payment',
                },
                'unit_amount': 2500,
            },
            'quantity': 1,
        }],
        allow_promotion_codes=True,
    )
    return HttpResponseRedirect(checkout_session.url)


@login_required
def checkout_success(request):
    session_id = request.GET.get('session_id')
    stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
    session = stripe.checkout.Session.retrieve(session_id, expand=['payment_intent'])
    assert len(session.payment_intent.charges.data) == 1
    charge_id = session.payment_intent.charges.data[0].id
    payment = Payment.objects.create(
        charge_id=charge_id,
        amount=session.amount_total,
        name='Payment from Checkout',
        user=request.user,
    )
    return HttpResponseRedirect(reverse('pegasus_examples:payment_confirm', args=[payment.payment_id]))


@login_required
def checkout_canceled(request):
    messages.info(request, 'Your payment was canceled.')
    return HttpResponseRedirect(reverse('pegasus_examples:payments'))
