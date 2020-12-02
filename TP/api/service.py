from django.db.models import Max, Q, Count
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
