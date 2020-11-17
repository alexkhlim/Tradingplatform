from django.db import models

from django.contrib.auth.models import User


class StockBase(models.Model):
    code = models.CharField('Code', max_length=8, unique=True)
    name = models.CharField('Name', max_length=128, unique=True)

    class Meta:
        abstract = True


class Currency(StockBase):

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Currency'
        verbose_name_plural = 'Currencies'


class Item(StockBase):
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    currency = models.ForeignKey(
        Currency, blank=True, null=True, on_delete=models.SET_NULL
    )
    details = models.TextField('Details', blank=True, null=True, max_length=512)

    def __str__(self):
        return self.code


class WatchList(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.user}, {self.item}'


class Price(models.Model):
    currency = models.ForeignKey(
        Currency, blank=True, null=True, on_delete=models.SET_NULL, related_name='currency'
    )
    item = models.ForeignKey(
        Item,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='prices',
        related_query_name='prices',
    )
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    date = models.DateTimeField(
        unique=True,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f'{self.item}, {self.price}{self.currency}'


class Offer(models.Model):
    CREATED = 0
    IN_PROCESS = 1
    DONE = 2

    ORDER_TYPE = [
        (CREATED, 'Created'),
        (IN_PROCESS, 'In process'),
        (DONE, 'Done'),
    ]

    BUY = 1
    SALE = 2

    OFFER_TYPE = (
        (BUY, BUY),
        (SALE, SALE),
    )

    offer_type = models.CharField(max_length=5, choices=OFFER_TYPE)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='user_offer')
    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.SET_NULL, related_name='item_offer')
    entry_quantity = models.IntegerField('Requested quantity')
    quantity = models.IntegerField('Current quantity', default=0)
    order_type = models.PositiveSmallIntegerField(choices=ORDER_TYPE, default=0)
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user}, {self.item}, {self.order_type}, {self.price}, {self.entry_quantity}'


class Trade(models.Model):
    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.SET_NULL)
    seller = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='seller_trade',
        related_query_name='seller_trade',
    )
    buyer = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='buyer_trade',
        related_query_name='buyer_trade',
    )
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    seller_offer = models.ForeignKey(
        Offer,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='seller_trade',
        related_query_name='seller_trade',
    )
    buyer_offer = models.ForeignKey(
        Offer,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='buyer_trade',
        related_query_name='buyer_trade',
    )

    def __str__(self):
        return f'{self.seller}, {self.buyer}, {self.quantity}'


class Inventory(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='user_inventory')
    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.SET_NULL, related_name='item_inventory')
    quantity = models.IntegerField('Stocks quantity', default=0)

    def __str__(self):
        return f'{self.user}, {self.item}, {self.quantity}'
