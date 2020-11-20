from django.contrib.auth.models import User
from django.db.models import Max
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (CreateModelMixin,
                                   ListModelMixin,
                                   RetrieveModelMixin,
                                   UpdateModelMixin,
                                   DestroyModelMixin)
from rest_framework import permissions, status
from api.serializers import *
from app.models import Trade, Offer, Currency, Inventory, Item, WatchList, Price
from api.service import Statistics


class CurrencyView(GenericViewSet, ListModelMixin, CreateModelMixin):
    queryset = Currency.objects.all()
    default_serializer_class = CurrencySerializer
    serializer_class = {
        'list': CurrencySerializer,
        'create': CurrencySerializer,
    }

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        return self.serializer_class.get(self.action, self.default_serializer_class)

    def get_paginated_response(self, data):
        return Response(data)


class ItemView(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = Item.objects.all()
    default_serializer_class = ItemListSerializer
    serializer_class = {
        'create': ItemSerializer,
        'retrieve': ItemRetrieveSerializer,
    }
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        return self.serializer_class.get(self.action, self.default_serializer_class)

    def get_paginated_response(self, data):
        return Response(data)


class WatchListView(GenericViewSet, ListModelMixin, CreateModelMixin,
                    RetrieveModelMixin, UpdateModelMixin):
    queryset = WatchList.objects.all()
    default_serializer_class = WatchListSerializer
    serializer_class = {
        'list': WatchListSerializer,
        'create': WatchListSerializer,
        'retrieve': WatchListSerializer,
        'update': WatchListSerializer,
    }
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        return self.serializer_class.get(self.action, self.default_serializer_class)

    def get_paginated_response(self, data):
        return Response(data)


class OfferView(GenericViewSet, ListModelMixin, CreateModelMixin):
    queryset = Offer.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('id', 'item_id', 'price')
    # ordering_fields = ['user_id', 'offer_type', 'entry_quantity', 'order_type', 'price']
    # ordering = ['user_id']
    default_serializer_class = OfferSerializer
    serializer_class = {
        'list': OfferListSerializer,
        'create': OfferCreateSerializer,
    }
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        return self.serializer_class.get(self.action, self.default_serializer_class)

    def get_paginated_response(self, data):
        return Response(data)

    def get_queryset(self):
        queryset = Offer.objects.all()
        params = self.request.query_params
        sort = params.getlist('sort', None)
        if sort:
            queryset = queryset.order_by(*sort)
        return queryset


class PriceDetail(GenericViewSet):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer

    def get_paginated_response(self, data):
        return Response(data)


class TradeViewSet(GenericViewSet):
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_paginated_response(self, data):
        return Response(data)


class InventoryViewSet(GenericViewSet, ListModelMixin, CreateModelMixin, RetrieveModelMixin):
    queryset = Inventory.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('user_id', 'id')
    default_serializer_class = InventorySerializer
    serializer_class = {
        'list': InventorySerializer,
        'create': InventorySerializer,
        'retrieve': InventorySerializer,
    }
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        return self.serializer_class.get(self.action, self.default_serializer_class)

    def get_paginated_response(self, data):
        return Response(data)


class SatisticsItemView(GenericViewSet, ListModelMixin):
    queryset = Item.objects.all()
    default_serializer_class = ItemListSerializer
    serializer_class = {
        'list': ItemListSerializer,
    }

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        return self.serializer_class.get(self.action, self.default_serializer_class)

    def get_paginated_response(self, data):
        return Response(data)

    def get_queryset(self):
        queryset = Statistics.most_popular()
        return queryset

    def list(self, request, *args, **kwargs):
        return Response(
            dict(
                most_expensive_item=Statistics.most_expensive_item(), most_popular=Statistics.most_popular()),
            status=HTTP_200_OK
        )
