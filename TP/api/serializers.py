from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from app.models import Trade, Offer, Currency, Inventory, Item, WatchList, Price


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserListSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name')


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
        fields = ('order_type', 'user', 'item')


class OfferCreateSerializer(ModelSerializer):
    class Meta:
        model = Offer
        fields = ('user', 'item', 'entry_quantity', 'quantity', 'price')


class TradeSerializer(ModelSerializer):
    class Meta:
        model = Trade
        fields = '__all__'


class InventorySerializer(ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'
