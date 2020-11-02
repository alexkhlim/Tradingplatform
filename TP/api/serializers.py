from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from app.models import Trade, Offer, Currency, Inventory, Item, WatchList, Price



class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name')


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
        fields = ('url', 'code', 'name')


class CurrencyDetailSerializer(ModelSerializer):
    class Meta:
        model = Currency
        fields = ('code', 'name')


class ItemSerializer(ModelSerializer):
    class Meta:
        model = Item
        fields = ('url', 'code', 'name', 'price', 'currency')


class ItemDetailSerializer(ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'


class WatchListSerializer(ModelSerializer):
    class Meta:
        model = WatchList
        fields = ('url', 'user', 'item')


class WatchListDetailSerializer(ModelSerializer):

    class Meta:
        model = WatchList
        fields = '__all__'


class PriceSerializer(ModelSerializer):
    class Meta:
        model = Price
        fields = '__all__'

class PriceDetailSerializer(ModelSerializer):
    class Meta:
        model = Price
        fields = '__all__'


class OfferSerializer(ModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'


class TradeSerializer(ModelSerializer):
    class Meta:
        model = Trade
        fields = '__all__'


class InventorySerializer(ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'
