from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.serializers import ModelSerializer
from rest_framework.response import Response
from rest_framework import status, serializers
from app.models import Trade, Offer, Currency, Inventory, Item, WatchList, Price
from api.tasks import create_trade
from api.service import Statistics


class UsersSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


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
        fields = ('id', 'code', 'name', 'price')


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
        fields = ('order_type', 'user', 'item', 'offer_type', 'entry_quantity', 'price')


class OfferCreateSerializer(ModelSerializer):
    class Meta:
        model = Offer
        fields = ('user', 'item', 'entry_quantity', 'quantity', 'offer_type', 'price')

    def create(self, validated_data):
        user_inventory = get_object_or_404(
            Inventory,
            user_id=validated_data.get('user').id,
            item_id=validated_data.get('item').id,
        )
        entry_quantity = validated_data['entry_quantity']
        if user_inventory.quantity < entry_quantity and validated_data.get('offer_type') == Offer.SALE:
            raise serializers.ValidationError('Not enough item')
        Offer.objects.create(
            user_id=validated_data.get('user').id,
            item_id=validated_data.get('item').id,
            entry_quantity=entry_quantity,
            quantity=validated_data.get('quantity'),
            price=validated_data.get('price'),
            offer_type=validated_data.get('offer_type')
        )
        if validated_data.get('offer_type') == Offer.SALE:
            user_inventory.quantity -= entry_quantity
            user_inventory.save(update_fields=('quantity',))
        return validated_data


class TradeSerializer(ModelSerializer):
    class Meta:
        model = Trade
        fields = '__all__'


class InventorySerializer(ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'

    def create(self, validated_data):
        try:
            inventory = Inventory.objects.get_or_create(
                user_id=validated_data.get('user').id,
                item_id=validated_data.get('item').id
            )
        except Inventory.DoesNotExist:
            raise serializers.ValidationError('there is no such user or item')
        inventory[0].quantity += validated_data.get('quantity')
        inventory[0].save(update_fields=('quantity',))
        Statistics.lolo()
        return inventory[0]
