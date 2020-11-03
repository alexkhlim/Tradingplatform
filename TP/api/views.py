from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework import permissions, status
from api.serializers import *
from app.models import Trade, Offer, Currency, Inventory, Item, WatchList, Price


class UserView(GenericViewSet, ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin):
    queryset = User.objects.all()
    default_serializer_class = UserSerializer
    serializer_class = {
        'list': UserListSerializer,
        'create': UserSerializer,
        'retrieve': UserSerializer,
        'update': UserUpdateSerializer,
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


class ItemView(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = Item.objects.all()
    default_serializer_class = CurrencySerializer
    serializer_class = {
        'create': ItemSerializer,
        'retrieve': ItemRetrieveSerializer,
    }
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        return self.serializer_class.get(self.action, self.default_serializer_class)


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


class OfferView(GenericViewSet, ListModelMixin, CreateModelMixin):
    queryset = Offer.objects.all()
    default_serializer_class = OfferSerializer
    serializer_class = {
        'list': OfferListSerializer,
        'create': OfferCreateSerializer,
    }
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        return self.serializer_class.get(self.action, self.default_serializer_class)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        inv = Inventory.objects.get(user_id=request.data.get('user'), item_id=request.data.get('item'))
        x = request.data.get('entry_quantity')
        if inv.quantity < int(x):
            raise (ValueError('Not enough item'))
        else:
            Offer.objects.create(
                user=User.objects.get(id=request.data.get('user')),
                item=Item.objects.get(id=request.data.get('item')),
                entry_quantity=request.data.get('entry_quantity'),
                quantity=request.data.get('quantity'),
                price=request.data.get('price'),
            )
            inv.quantity -= int(request.data.get('entry_quantity'))
            inv.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PriceDetail(GenericViewSet):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer


class TradeViewSet(GenericViewSet):
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class InventoryViewSet(GenericViewSet, ListModelMixin, CreateModelMixin, RetrieveModelMixin):
    queryset = Inventory.objects.all()
    default_serializer_class = InventorySerializer
    serializer_class = {
        'list': InventorySerializer,
        'create': InventorySerializer,
        'retrieve': InventorySerializer,
    }
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        return self.serializer_class.get(self.action, self.default_serializer_class)
