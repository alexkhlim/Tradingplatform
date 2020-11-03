from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework import permissions
from api.serializers import *
from app.models import Trade, Offer, Currency, Inventory, Item, WatchList, Price


class UserListCreateDetailUpdateView(GenericViewSet, ListModelMixin, CreateModelMixin, RetrieveModelMixin,
                                     UpdateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.queryset
        serializer = UserListSerializer(queryset, many=True)
        return Response(serializer.data)


class CurrencyListCreateView(GenericViewSet, ListModelMixin):
    """2 fields, don't need an additional serializer"""
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class ItemCreateListDetailView(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.queryset
        serializer = ItemListSerializer(queryset, many=True)
        return Response(serializer.data)


class WatchListCreateListDetailUpdateView(GenericViewSet, ListModelMixin, CreateModelMixin,
                                          RetrieveModelMixin, UpdateModelMixin):
    """2 fields, don't need an additional serializer"""
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer


class OfferListCreateView(GenericViewSet, ListModelMixin, CreateModelMixin):
    queryset = Offer.objects.all()
    serializer_class = OfferCreateSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.queryset
        serializer = OfferListSerializer(queryset, many=True)
        return Response(serializer.data)


class PriceDetail(GenericViewSet):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer


class TradeViewSet(GenericViewSet):
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class InventoryViewSet(GenericViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
