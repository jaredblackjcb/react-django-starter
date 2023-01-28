from django.urls import path
from django.views.generic import TemplateView

from . import views


app_name = 'pegasus_examples'

urlpatterns = [
    path('', views.ExamplesHomeView.as_view(), name='examples_home'),
    path('payments', views.PaymentView.as_view(), name='payments'),
    # payments via elements
    path('payments/create_payment_intent/', views.create_payment_intent, name='create_payment_intent'),
    path('payments/create/', views.accept_payment, name='accept_payment'),
    path('payments/confirm/<slug:payment_id>/', views.payment_confirm, name='payment_confirm'),
    # payments via checkout
    path('payments/create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('payments/checkout-success/', views.checkout_success, name='checkout_success'),
    path('payments/checkout-canceled/', views.checkout_canceled, name='checkout_canceled'),

    path('landing-page/', TemplateView.as_view(template_name='pegasus/examples/example_landing_page.html',
                                               extra_context={'active_tab': 'landing_page'}),
         name='landing_page'),
    path('pricing-page/', TemplateView.as_view(template_name='pegasus/examples/example_pricing_page.html',
                                               extra_context={'active_tab': 'pricing_page'}),
         name='pricing_page'),

    # these are experimental examples that aren't currently exposed in the UI.
    path('alpine/', TemplateView.as_view(template_name='pegasus/examples/alpine_demo.html'), name='alpine_demo'),
    path('forms/', views.ExampleFormView.as_view(), name='form_demo'),

    # tasks
    path('tasks/', views.TasksView.as_view(), name='tasks'),
    path('tasks/api/', views.tasks_api, name='tasks_api'),

    # flags
    path('flags/', views.FeatureFlagExampleView.as_view(), name='flags')
]
