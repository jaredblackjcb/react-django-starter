import rest_framework.serializers
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework.response import Response
from rest_framework.views import APIView

from ..exceptions import SubscriptionConfigError
from ..helpers import create_stripe_checkout_session, create_stripe_portal_session
from ..metadata import get_active_products_with_metadata, ProductWithMetadata


class ProductWithMetadataAPI(APIView):

    @extend_schema(
        operation_id='active_products_list',
        responses={
            200: ProductWithMetadata.serializer()
        }
    )
    def get(self, request, *args, **kw):
        products_with_metadata = get_active_products_with_metadata()
        return Response(
            data=[p.to_dict() for p in products_with_metadata]
        )


@extend_schema(
    tags=["subscriptions"]
)
class CreateCheckoutSession(APIView):

    @extend_schema(
        operation_id='create_checkout_session',
        request=inline_serializer("CreateCheckout", {
            'priceid': rest_framework.serializers.CharField()
        }),
        responses={
            200: OpenApiTypes.URI,
        },
    )
    def post(self, request):
        subscription_holder = request.user
        price_id = request.POST['priceId']
        checkout_session = create_stripe_checkout_session(
            subscription_holder, price_id, request.user,
        )
        return Response(checkout_session.url)


@extend_schema(
    tags=["subscriptions"]
)
class CreatePortalSession(APIView):

    @extend_schema(
        operation_id='create_portal_session',
        request=None,
        responses={
            200: OpenApiTypes.URI,
        },
    )
    def post(self, request):
        subscription_holder = request.user
        try:
            portal_session = create_stripe_portal_session(subscription_holder)
            return Response(portal_session.url)
        except SubscriptionConfigError as e:
            return Response(str(e), status=500)
