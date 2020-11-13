from app.models import *
from celery import shared_task
from api.service import TradeService
@shared_task()
def create_trade():
    buy_offers = Offer.objects.filter(offer_type=Offer.BUY)
    for buy_offer in buy_offers:
        if buy_offer.order_type != Offer.DONE:
            buy_offer.order_type = Offer.IN_PROCESS
            buy_offer.save()
            user_inventory = Inventory.objects.get(user_id=buy_offer.user.id, item_id=buy_offer.item.id)
            sale_offers = Offer.objects.filter(offer_type=Offer.SALE, item=buy_offer.item).order_by('price')
            for sale_offer in sale_offers:
                if sale_offer.price <= buy_offer.price and sale_offer.order_type != Offer.DONE:
                    TradeService.create_object_trade(buy_offer, sale_offer)
                    TradeService.operations_with_trade_data(buy_offer, sale_offer, user_inventory)
