from djstripe.models import Product, Subscription, Price, SubscriptionItem
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers


class PriceSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name')
    human_readable_price = serializers.SerializerMethodField()

    @extend_schema_field(OpenApiTypes.STR)
    def get_human_readable_price(self, obj):
        # this needs to be here because djstripe can return a proxy object which can't be serialized
        return str(obj.human_readable_price)

    class Meta:
        model = Price
        fields = ('id', 'product_name', 'human_readable_price', 'nickname', 'unit_amount')


class SubscriptionItemSerializer(serializers.ModelSerializer):
    price = PriceSerializer()

    class Meta:
        model = SubscriptionItem
        fields = ('id', 'price', 'quantity')


class SubscriptionSerializer(serializers.ModelSerializer):
    """
    A serializer for Subscriptions which uses the SubscriptionWrapper object under the hood
    """
    items = SubscriptionItemSerializer(many=True)
    display_name = serializers.CharField()
    billing_interval = serializers.CharField()

    class Meta:
        # we use Subscription instead of SubscriptionWrapper so DRF can infer the model-based fields automatically
        model = Subscription
        fields = ('id', 'display_name', 'start_date', 'billing_interval', 'current_period_start',
                  'current_period_end', 'cancel_at_period_end', 'start_date', 'status', 'quantity', 'items')


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'name')
