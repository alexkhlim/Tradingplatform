from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import Http404
from rest_framework.serializers import ModelSerializer
from rest_framework.response import Response
from rest_framework import status
from app.models import Trade, Offer, Currency, Inventory, Item, WatchList, Price


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserListSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name')


class UserUpdateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email')


class CreateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class CurrencySerializer(ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'


class ItemSerializer(ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class ItemListSerializer(ModelSerializer):
    class Meta:
        model = Item
        fields = ('code', 'name', 'price')


class ItemRetrieveSerializer(ModelSerializer):
    class Meta:
        model = Item
        fields = ('name', 'price', 'currency', 'details')


class WatchListSerializer(ModelSerializer):
    class Meta:
        model = WatchList
        fields = '__all__'


class PriceSerializer(ModelSerializer):
    class Meta:
        model = Price
        fields = '__all__'


class OfferSerializer(ModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'


class OfferListSerializer(ModelSerializer):
    class Meta:
        model = Offer
        fields = ('order_type', 'user', 'item', 'Offer_type', 'entry_quantity')


class OfferCreateSerializer(ModelSerializer):
    class Meta:
        model = Offer
        fields = ('user', 'item', 'entry_quantity', 'quantity', 'Offer_type', 'price')

    def create(self, validated_data):
        user_inventory = Inventory.objects.get(user_id=validated_data.get('user').id,
                                               item_id=validated_data.get('item').id)
        entry_quantity = validated_data['entry_quantity']
        if user_inventory.quantity < entry_quantity and validated_data.get('Offer_type') == 'sale':
            raise (ValueError('Not enough item'))
        try:
            Offer.objects.create(
                user_id=validated_data.get('user').id,
                item_id=validated_data.get('item').id,
                entry_quantity=entry_quantity,
                quantity=validated_data.get('quantity'),
                price=validated_data.get('price'),
                Offer_type=validated_data.get('Offer_type')
            )
            if validated_data.get('Offer_type') == 'sale':
                user_inventory.quantity -= entry_quantity
                user_inventory.save()
            return validated_data
        except IntegrityError:
            raise (Http404('there is no such user or item'))


class TradeSerializer(ModelSerializer):
    class Meta:
        model = Trade
        fields = '__all__'


class InventorySerializer(ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'

    def create(self, validated_data):
        inv = 0
        try:
            inv = Inventory.objects.get(user_id=validated_data.get('user').id, item_id=validated_data.get('item').id)
        except:
            pass
        if bool(inv):
            inv.quantity += validated_data.get('quantity')
            inv.save()
            return inv
        else:
            try:
                Inventory.objects.create(
                    user_id=validated_data.get('user').id,
                    item_id=validated_data.get('item').id,
                    quantity=validated_data.get('quantity'),
                )
                return validated_data
            except IntegrityError:
                raise (Http404('there is no such user or item'))
