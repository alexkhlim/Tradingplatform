import csv
import io
from django.db.models import Max, Q, Count
from django.db import connection
from app.models import *
from datetime import datetime


class TradeService:

    @staticmethod
    def create_object_trade(buy_offer, sale_offer):
        quantity_buy = buy_offer.entry_quantity
        quantity_sale = sale_offer.entry_quantity
        if quantity_buy > quantity_sale:
            quantity_trade = quantity_sale
        else:
            quantity_trade = quantity_buy
        fields = ([buy_offer.item.id,
                   sale_offer.user,
                   buy_offer.user,
                   quantity_trade,
                   sale_offer.price,
                   sale_offer,
                   buy_offer,
                   f'{buy_offer.user} bought {quantity_trade} shares from \
                         {sale_offer.user} for {sale_offer.price * quantity_trade} in {datetime.now()}'
                   ])
        return fields

    @staticmethod
    def operations_with_trade_data(buy_offer, sale_offer, user_inventory):
        quantity_buy = buy_offer.entry_quantity
        quantity_sale = sale_offer.entry_quantity
        if quantity_buy > quantity_sale:
            buy_offer.entry_quantity -= sale_offer.entry_quantity
            user_inventory.quantity += sale_offer.entry_quantity
            sale_offer.order_type = Offer.DONE
            sale_offer.entry_quantity = 0

        elif quantity_buy < quantity_sale:
            sale_offer.entry_quantity -= buy_offer.entry_quantity
            user_inventory.quantity += buy_offer.entry_quantity
            buy_offer.order_type = Offer.DONE
            buy_offer.entry_quantity = 0

        else:
            user_inventory.quantity += sale_offer.entry_quantity
            buy_offer.entry_quantity = 0
            sale_offer.entry_quantity = 0
            sale_offer.order_type = Offer.DONE
            buy_offer.order_type = Offer.DONE

        buy_offer.save(update_fields=('entry_quantity', 'order_type'))
        user_inventory.save(update_fields=('quantity',))
        sale_offer.save(update_fields=('entry_quantity', 'order_type'))


class Statistics:

    @staticmethod
    def most_expensive_item():
        return Item.objects.filter(price=Item.objects.aggregate(Max('price'))['price__max']).values()

    @staticmethod
    def most_popular():
        return Item.objects.annotate(
            num_inv=Count('item_inventory', filter=Q(item_inventory__quantity__gt=0))
        ).order_by('-num_inv')[:3].values()


def cursor_copy_from(file, table, sep, columns):
    file.seek(0)
    cursor = connection.cursor()
    cursor.copy_from(
        file=file,
        table=table,
        sep=sep,
        columns=columns,
    )


def data_recording(iter_obj, user):
    stream = io.StringIO()
    writer = csv.writer(stream, delimiter=',')
    for obj in iter_obj:
        writer.writerow([user.id, obj.id, 0])
    return stream
