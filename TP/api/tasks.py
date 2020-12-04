from django.db.models import Count
import csv
import io
from django.db import connection
from celery import shared_task
from app.models import *
from api.service import TradeService


@shared_task()
def create_trade():
    stream = io.StringIO()
    writer = csv.writer(stream, delimiter=',')
    items = Item.objects.annotate(num_offers=Count('item_offer')).exclude(num_offers=0)
    for item in items:
        buy_offers = Offer.objects.filter(offer_type=Offer.BUY, item=item).exclude(order_type=Offer.DONE)
        sale_offers = Offer.objects.filter(offer_type=Offer.SALE, item=item).exclude(order_type=Offer.DONE).order_by(
            'price')
        for buy_offer in buy_offers.iterator():
            user_inventory, create = Inventory.objects.get_or_create(user_id=buy_offer.user.id,
                                                                     item_id=buy_offer.item.id)
            for sale_offer in sale_offers.iterator():
                if sale_offer.price <= buy_offer.price:
                    writer.writerow(TradeService.create_object_trade(buy_offer, sale_offer))
                    TradeService.operations_with_trade_data(buy_offer, sale_offer, user_inventory)
    columns = (
        'item_id',
        'seller_id',
        'buyer_id',
        'quantity',
        'unit_price',
        'seller_offer_id',
        'buyer_offer_id',
        'description'
    )
    cursor = connection.cursor()
    cursor.copy_from(
        file=stream,
        table='app_trade',
        sep=',',
        columns=columns,
    )
