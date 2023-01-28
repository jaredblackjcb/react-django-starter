from django.core.management import call_command
from django.core.management.base import BaseCommand
from djstripe.models import Product, APIKey
from djstripe.settings import djstripe_settings
from stripe.error import AuthenticationError

from apps.subscriptions.metadata import ProductMetadata


class Command(BaseCommand):
    help = 'Bootstraps your Stripe subscriptions'

    def handle(self, **options):
        print('Syncing products and plans from Stripe')
        try:
            _create_api_keys_if_necessary()
            call_command('djstripe_sync_plans_from_stripe')
        except AuthenticationError:
            print('\n======== ERROR ==========\n'
                  'Failed to authenticate with Stripe! Check your Stripe key settings.\n'
                  'More info: https://docs.saaspegasus.com/subscriptions.html#getting-started')
        else:
            print('Done! Creating default product configuration')
            _create_default_product_config()


def _create_api_keys_if_necessary():
    key, created = APIKey.objects.get_or_create_by_api_key(djstripe_settings.STRIPE_SECRET_KEY)
    if created:
        print('Added Stripe secret key to the database...')


def _create_default_product_config():
    # make the first product the default
    default = True
    product_metas = []
    for product in Product.objects.filter(active=True):
        product_meta = ProductMetadata.from_stripe_product(
            product,
            description=f'The {product.name} plan',
            is_default=default,
            features=[
                "{} Feature 1".format(product.name),
                "{} Feature 2".format(product.name),
                "{} Feature 3".format(product.name),
            ]
        )
        default = False
        product_metas.append(product_meta)

    print('Copy/paste the following code into your `apps/subscriptions/metadata.py` file:\n\n')
    newline = '\n'
    print(f'ACTIVE_PRODUCTS = [{newline}    {f",{newline}    ".join(str(meta) for meta in product_metas)},{newline}]')
