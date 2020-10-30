from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework import generics, permissions
from api.serializers import (
    TradeSerializer,
    WatchListSerializer,
    PriceSerializer,
    ItemSerializer,
    OfferSerializer,
    InventorySerializer,
    UserSerializer,
    CurrencySerializer,
    CreateUserSerializer,
    CurrencyDetailSerializer,
    ItemDetailSerializer,
    WatchListDetailSerializer,
    PriceDetailSerializer
)
from app.models import Trade, Offer, Currency, Inventory, Item, WatchList, Price


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CreateUserView(generics.CreateAPIView, CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (permissions.AllowAny,)


class CurrencyViewSet(ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CreateCurrencyView(generics.CreateAPIView, CreateModelMixin):
    queryset = Currency.objects.all()
    serializer_class = CurrencyDetailSerializer


class CurrencyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencyDetailSerializer


class ItemViewSet(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CreateItemView(generics.CreateAPIView, CreateModelMixin):
    queryset = Item.objects.all()
    serializer_class = ItemDetailSerializer


class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemDetailSerializer


class WatchListViewSet(ModelViewSet):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CreateWatchListView(generics.CreateAPIView, CreateModelMixin):
    queryset = WatchList.objects.all()
    serializer_class = WatchListDetailSerializer


class WatchListDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListDetailSerializer


class PriceViewSet(ModelViewSet):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class PriceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Price.objects.all()
    serializer_class = PriceDetailSerializer


class OfferViewSet(ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TradeViewSet(ModelViewSet):
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class InventoryViewSet(ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
