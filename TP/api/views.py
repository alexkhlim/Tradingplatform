from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet, ViewSetMixin, GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework import generics, permissions
from api.serializers import *
from app.models import Trade, Offer, Currency, Inventory, Item, WatchList, Price


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserListCreateView(generics.ListCreateAPIView, GenericViewSet, ListModelMixin, CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailUpdateView(generics.RetrieveUpdateAPIView, GenericViewSet, RetrieveModelMixin, UpdateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CurrencyViewSet(ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CurrencyListCreateView(generics.ListCreateAPIView, GenericViewSet, ListModelMixin, CreateModelMixin):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class CurrencyDetailUpdate(generics.RetrieveUpdateAPIView, GenericViewSet, RetrieveModelMixin, UpdateModelMixin):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class ItemViewSet(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ItemCreateListView(generics.CreateAPIView, GenericViewSet, CreateModelMixin, ListModelMixin):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class ItemDetail(generics.RetrieveAPIView, GenericViewSet, RetrieveModelMixin, UpdateModelMixin,
                 DestroyModelMixin):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class WatchListViewSet(ModelViewSet):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class WatchListCreateListView(generics.ListCreateAPIView, GenericViewSet, ListModelMixin, CreateModelMixin):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer


class WatchListDetailUpdate(generics.RetrieveUpdateAPIView, GenericViewSet, RetrieveModelMixin, UpdateModelMixin):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer


class PriceViewSet(ModelViewSet):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class PriceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer


class OfferViewSet(ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class OfferListCreateView(generics.ListCreateAPIView, GenericViewSet, ListModelMixin, CreateModelMixin):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer


class TradeViewSet(ModelViewSet):
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class InventoryViewSet(ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
