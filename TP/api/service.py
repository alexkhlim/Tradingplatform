from django.db.models import Max, Q, Count, Avg, Sum
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
        Trade.objects.create(
            item_id=buy_offer.item.id,
            seller=sale_offer.user,
            buyer=buy_offer.user,
            quantity=quantity_trade,
            unit_price=sale_offer.price,
            seller_offer=sale_offer,
            buyer_offer=buy_offer,
            description=f'{buy_offer.user} bought {quantity_trade} shares from \
            {sale_offer.user} for {sale_offer.price * quantity_trade} in {datetime.now()}'
        )

    @staticmethod
    def operations_with_trade_data(buy_offer, sale_offer, user_inventory):
        quantity_buy = buy_offer.entry_quantity
        quantity_sale = sale_offer.entry_quantity
        if quantity_buy > quantity_sale:
            buy_offer.entry_quantity -= sale_offer.entry_quantity
            user_inventory.quantity += sale_offer.entry_quantity
            sale_offer.entry_quantity = 0
            sale_offer.order_type = Offer.DONE
            buy_offer.save(update_fields=('entry_quantity',))
            user_inventory.save(update_fields=('quantity',))
            sale_offer.save()
        elif quantity_buy < quantity_sale:
            user_inventory.quantity += buy_offer.entry_quantity
            sale_offer.entry_quantity -= buy_offer.entry_quantity
            buy_offer.order_type = Offer.DONE
            buy_offer.entry_quantity = 0
            buy_offer.save()
            user_inventory.save(update_fields=('quantity',))
            sale_offer.save(update_fields=('entry_quantity',))
        else:
            user_inventory.quantity += sale_offer.entry_quantity
            buy_offer.entry_quantity = 0
            sale_offer.entry_quantity = 0
            sale_offer.order_type = Offer.DONE
            buy_offer.order_type = Offer.DONE
            buy_offer.save()
            user_inventory.save(update_fields=('quantity',))
            sale_offer.save()


class Statistics:

    @staticmethod
    def most_expensive_item():
        items = Item.objects.all()
        max_expensive = items.aggregate(Max('price'))
        return Item.objects.filter(price=max_expensive['price__max']).values()

    @staticmethod
    def most_popular():
        dict_items = {}
        inventorys = Item.objects.annotate(quantity_items=Count('item_inventory'))
        for inventory in inventorys:
            dict_items[inventory] = inventory.quantity_items
        max_count = max(dict_items.values())
        spis_item = []
        for key, value in dict_items.items():
            if value == max_count:
                spis_item.append(key)
        count_spis = len(spis_item)
        print(spis_item)
        if count_spis == 1:
            return Item.objects.filter(name=spis_item[0].name).values()
        elif count_spis == 2:
            return Item.objects.filter(
                Q(name=spis_item[0].name) | Q(name=spis_item[1].name)).values()
        else:
            return Item.objects.filter(
                Q(name=spis_item[0].name) | Q(name=spis_item[1].name) | Q(name=spis_item[2].name)
            ).values()
