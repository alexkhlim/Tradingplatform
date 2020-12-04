import csv
import io
from django.db import connection
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.serializers import ModelSerializer, ValidationError
from app.models import Trade, Offer, Currency, Inventory, Item, WatchList, Price
from .permissions import OfferValidation
from .service import cursor_copy_from, data_recording


class UsersSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name')
        # fields = '__all__'


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
        OfferValidation.checking_number_items(user_inventory.quantity, entry_quantity, validated_data.get('offer_type'))
        Offer.objects.create(**validated_data)
        OfferValidation.decrease_items(validated_data.get('offer_type'), user_inventory, entry_quantity)
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
            inventory, created = Inventory.objects.get_or_create(
                user_id=validated_data.get('user').id,
                item_id=validated_data.get('item').id
            )
        except Inventory.DoesNotExist:
            raise ValidationError('there is no such user or item')
        inventory.quantity += validated_data.get('quantity')
        inventory.save(update_fields=('quantity',))
        return inventory


class UserInventorySerializer(ModelSerializer):
    class Meta:
        model = Inventory
        fields = ('user', 'item', 'quantity')

    # def create(self, validated_data):
    #     Inventory.objects.to_csv('./data.csv')
    #     user = self.context['request'].user
    #     no_items_user = Item.objects.exclude(item_inventory__user_id=user.id)
    #     new_inventories = [(Inventory(user_id=user.id, item=item)) for item in no_items_user]
    #     inventories = Inventory.objects.bulk_create(new_inventories)
    #     return inventories

    def create(self, validated_data):
        user = self.context['request'].user
        no_items_user = Item.objects.exclude(item_inventory__user_id=user.id)
        stream = data_recording(no_items_user, user)
        cursor_copy_from(stream, 'app_inventory', ',', ('user_id', 'item_id', 'quantity'))
        return Inventory.objects.all()
