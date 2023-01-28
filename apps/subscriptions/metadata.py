from __future__ import annotations

from dataclasses import dataclass, asdict, field

from django.utils.functional import cached_property
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from djstripe.enums import PlanInterval
from djstripe.models import Product, Price
from typing import List, Generator, Dict

from .exceptions import SubscriptionConfigError
from .serializers import PriceSerializer, ProductSerializer


@dataclass
class ProductMetadata:
    """
    Metadata for a Stripe product.
    """
    stripe_id: str
    slug: str
    name: str
    features: List[str]
    price_displays: Dict[str: str] = field(default_factory=dict)
    description: str = ''
    is_default: bool = False

    @classmethod
    def from_stripe_product(cls, stripe_product: Product, **kwargs) -> ProductMetadata:
        defaults = dict(
            stripe_id=stripe_product.id,
            slug=slugify(stripe_product.name),
            name=stripe_product.name,
            features=[]
        )
        defaults.update(kwargs)
        return cls(
            **defaults
        )

    @classmethod
    def serializer(cls):
        """Serializer used for schema generation"""
        from drf_spectacular.utils import inline_serializer
        from rest_framework import serializers

        return inline_serializer('ProductMetadata', {
            'stripe_id': serializers.CharField(),
            'slug': serializers.CharField(),
            'name': serializers.CharField(),
            'features': serializers.ListField(child=serializers.CharField()),
            'price_displays': serializers.DictField(child=serializers.CharField()),
            'description': serializers.CharField(),
            'is_default': serializers.BooleanField(),
        })


@dataclass
class ProductWithMetadata(object):
    """
    Connects a Stripe product to its ProductMetadata.
    """
    product: Product
    metadata: ProductMetadata

    @property
    def stripe_id(self) -> str:
        return self.metadata.stripe_id or self.product.id

    @cached_property
    def default_price(self) -> Price:
        if not ACTIVE_PLAN_INTERVALS:
            raise SubscriptionConfigError(_('At least one plan interval (year or month) must be set!'))
        return self.monthly_price if ACTIVE_PLAN_INTERVALS[0] == PlanInterval.month else self.annual_price

    @cached_property
    def annual_price(self) -> Price:
        return self._get_price(PlanInterval.year)

    @cached_property
    def monthly_price(self) -> Price:
        return self._get_price(PlanInterval.month)

    def _get_price(self, interval: str) -> Price:
        if self.product:
            try:
                return self.product.prices.get(recurring__interval=interval, recurring__interval_count=1, active=True)
            except (Price.DoesNotExist, Price.MultipleObjectsReturned):
                raise SubscriptionConfigError(_(
                    f'Unable to select a "{interval}" plan for {self.product}. '
                    'Have you setup your Stripe objects and run ./manage.py bootstrap_subscriptions? '
                    'You can also hide this plan interval by removing it from ACTIVE_PLAN_INTERVALS in '
                    'apps/subscriptions/metadata.py'
                ))

    def get_annual_price_display(self) -> str:
        return self.get_price_display(self.annual_price)

    def get_monthly_price_display(self) -> str:
        return self.get_price_display(self.monthly_price)

    def get_price_display(self, price: Price) -> str:
        # if the price display info has been explicitly overridden, use that
        if price.recurring['interval'] in self.metadata.price_displays:
            return self.metadata.price_displays[price.recurring['interval']]
        else:
            # otherwise get it from the price
            from apps.subscriptions.helpers import get_friendly_currency_amount
            return get_friendly_currency_amount(price)

    def to_dict(self):
        """
        :return: a JSON-serializable dictionary for this object,
        usable in an API.
        """
        def _serialized_price_or_none(price):
            return PriceSerializer(price).data if price else None

        return {
            'product': ProductSerializer(self.product).data,
            'metadata': asdict(self.metadata),
            'default_price': _serialized_price_or_none(self.default_price),
            'annual_price': _serialized_price_or_none(self.annual_price),
            'monthly_price': _serialized_price_or_none(self.monthly_price),
        }

    @classmethod
    def serializer(cls):
        """Serializer used for schema generation"""
        from drf_spectacular.utils import inline_serializer
        return inline_serializer('ProductWithMetadata', {
                'product': ProductSerializer(),
                'metadata': ProductMetadata.serializer(),
                'default_price': PriceSerializer(),
                'annual_price': PriceSerializer(),
                'monthly_price': PriceSerializer(),
            })


@dataclass
class PlanIntervalMetadata(object):
    """
    Metadata for a Stripe product.
    """
    interval: str
    name: str


def get_plan_name_for_interval(interval: str) -> str:
    return {
        PlanInterval.year: _('Annual'),
        PlanInterval.month: _('Monthly'),
    }.get(interval, _('Custom'))


def get_active_plan_interval_metadata() -> List[PlanIntervalMetadata]:
    return [
        PlanIntervalMetadata(interval=interval, name=get_plan_name_for_interval(interval))
        for interval in ACTIVE_PLAN_INTERVALS
    ]

# Active plan intervals. Only allowed values are "PlanInterval.month" and "PlanInterval.year"
# Remove one of them to only allow monthly/annual pricing.
# The first element is considered the default
ACTIVE_PLAN_INTERVALS = [
    PlanInterval.year,
    PlanInterval.month,
]


# These are the products that will be shown to users in the UI and allowed to be associated
# with plans on your side
ACTIVE_PRODUCTS = [
    ProductMetadata(
        stripe_id='',
        slug='starter',
        name=_('Starter'),
        description=_('For hobbyists and side-projects'),
        features=[
            _('Up to 100 Widgets'),
            _('Unlimited Widget Editing'),
        ],
    ),
    ProductMetadata(
        stripe_id='',
        slug='standard',
        name=_('Standard'),
        description=_('For small businesses and teams'),
        is_default=True,
        features=[
            _('Up to 500 Widgets'),
            _('Unlimited Widget Editing'),
            _('Advanced Widget Editing Features'),
        ],
    ),
    ProductMetadata(
        stripe_id='',
        slug='premium',
        name=_('Premium'),
        description=_('For small businesses and teams'),
        features=[
            _('Unlimited Widgets'),
            _('All Features'),
            _('Priority Support and Training'),
        ],
    ),
]

ACTIVE_PRODUCTS_BY_ID = {
    p.stripe_id: p for p in ACTIVE_PRODUCTS
}


def get_active_products_with_metadata() -> Generator[ProductWithMetadata]:
    # if we have set active products in metadata then filter the full list
    if ACTIVE_PRODUCTS:
        for product_meta in ACTIVE_PRODUCTS:
            try:
                yield ProductWithMetadata(
                    product=Product.objects.get(id=product_meta.stripe_id),
                    metadata=product_meta,
                )
            except Product.DoesNotExist:
                raise SubscriptionConfigError(_(
                    f'No Product with ID "{product_meta.stripe_id}" found! '
                    f'This is coming from the "{product_meta.name}" Product in the ACTIVE_PRODUCTS variable '
                    f'in metadata.py. '
                    f'Please make sure that all products in ACTIVE_PRODUCTS have a valid stripe_id and that '
                    f'you have synced your Product database with Stripe.'
                ))
    else:
        # otherwise just use whatever is in the DB
        for product in Product.objects.all():
            yield ProductWithMetadata(
                product=product,
                metadata=ACTIVE_PRODUCTS_BY_ID.get(product.id, ProductMetadata.from_stripe_product(product))
            )
        else:
            raise SubscriptionConfigError(_(
                'It looks like you do not have any Products in your database. '
                'In order to use subscriptions you first have to setup Stripe billing and sync it '
                'with your local data.'
            ))


def get_product_with_metadata(djstripe_product: Product) -> ProductWithMetadata:
    if djstripe_product.id in ACTIVE_PRODUCTS_BY_ID:
        return ProductWithMetadata(
            product=djstripe_product,
            metadata=ACTIVE_PRODUCTS_BY_ID[djstripe_product.id]
        )
    else:
        return ProductWithMetadata(
            product=djstripe_product,
            metadata=ProductMetadata.from_stripe_product(djstripe_product)
        )
