from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (CreateModelMixin,
                                   ListModelMixin,
                                   RetrieveModelMixin,
                                   UpdateModelMixin,
                                   DestroyModelMixin)
from rest_framework import permissions, status
from rest_framework.response import Response
from api.serializers import *
from app.models import Trade, Offer, Currency, Inventory, Item, WatchList, Price, Office
from api.service import Statistics
from .permissions import has_action


class UserView(GenericViewSet, ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin):
    queryset = User.objects.all()
    default_serializer_class = UsersSerializer
    serializer_class = {
        'list': UsersSerializer,
        'create': UsersSerializer,
        'retrieve': UsersSerializer,
        'update': UsersSerializer,
    }
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        return self.serializer_class.get(self.action, self.default_serializer_class)


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


class ItemView(GenericViewSet, CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin):
    queryset = Item.objects.all()
    default_serializer_class = ItemListSerializer
    serializer_class = {
        'create': ItemSerializer,
        'retrieve': ItemRetrieveSerializer,
        'update': ItemRetrieveSerializer
    }

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        return self.serializer_class.get(self.action, self.default_serializer_class)

    def get_paginated_response(self, data):
        return Response(data)

    def create(self, request):
        if not has_action(request.user, model_name='item', permission_type='can_create'):
            return Response({}, status=status.HTTP_403_FORBIDDEN)

        return super().create(request)

    def update(self, request, *args, **kwargs):
        if not Office.objects.filter(user=self.request.user).exists():
            return Response({}, status=status.HTTP_403_FORBIDDEN)

        if not has_action(request.user, Office.objects.get(user=self.request.user), self.get_object(), 'item',
                          'can_update'):
            return Response({}, status=status.HTTP_403_FORBIDDEN)

        return super().update(request)


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


class UserInventoryView(GenericViewSet, ListModelMixin, CreateModelMixin):
    queryset = Inventory.objects.all()
    default_serializer_class = UserInventorySerializer
    serializer_class = {
        'list': UserInventorySerializer,
    }

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        return self.serializer_class.get(self.action, self.default_serializer_class)

    def get_paginated_response(self, data):
        return Response(data)

    def list(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return Response({'an unauthenticated user'}, status=status.HTTP_403_FORBIDDEN)

        return super().list(request)

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Inventory.objects.all()

        return Inventory.objects.filter(user=self.request.user)
