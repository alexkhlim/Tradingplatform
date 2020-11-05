from django.db import IntegrityError
from django.http import Http404
from app.models import *


def create_trade():
    buy_offers = Offer.objects.filter(Offer_type='buy')
    for buy_offer in buy_offers:
        if buy_offer.order_type != 2:
            buy_offer.order_type = 1
            buy_offer.save()
            user_inventory = Inventory.objects.get(user_id=buy_offer.user.id, item_id=buy_offer.item.id)
            sale_offers = Offer.objects.filter(Offer_type='sale', item=buy_offer.item).order_by('price')
            for sale_offer in sale_offers:
                if sale_offer.price <= buy_offer.price and sale_offer.order_type != 2:
                    if buy_offer.entry_quantity < sale_offer.entry_quantity:
                        try:
                            Trade.objects.create(
                                item_id=buy_offer.item.id,
                                seller=sale_offer.user,
                                buyer=buy_offer.user,
                                quantity=buy_offer.entry_quantity,
                                unit_price=sale_offer.price,
                                seller_offer=sale_offer,
                                buyer_offer=buy_offer,
                                description=f'{buy_offer.user} bought {sale_offer.entry_quantity} shares from \
                                {sale_offer.user} for {sale_offer.price * buy_offer.entry_quantity}'
                            )
                        except IntegrityError:
                            raise (Http404('there is no such user or item'))
                        user_inventory.quantity += sale_offer.entry_quantity
                        sale_offer.entry_quantity -= buy_offer.entry_quantity
                        buy_offer.order_type = 2
                        buy_offer.entry_quantity = 0
                        buy_offer.save()
                        user_inventory.save()
                        sale_offer.save()
                        continue
                    elif buy_offer.entry_quantity == sale_offer.entry_quantity:
                        try:
                            Trade.objects.create(
                                item_id=buy_offer.item.id,
                                seller=sale_offer.user,
                                buyer=buy_offer.user,
                                quantity=buy_offer.entry_quantity,
                                unit_price=sale_offer.price,
                                seller_offer=sale_offer,
                                buyer_offer=buy_offer,
                                description=f'{buy_offer.user} bought {sale_offer.entry_quantity} shares from \
                                {sale_offer.user} for {sale_offer.price * buy_offer.entry_quantity}'
                            )
                        except IntegrityError:
                            raise (Http404('there is no such user or item'))
                        user_inventory.quantity += sale_offer.entry_quantity
                        buy_offer.entry_quantity = 0
                        sale_offer.entry_quantity = 0
                        sale_offer.order_type = 2
                        buy_offer.order_type = 2
                        buy_offer.save()
                        user_inventory.save()
                        sale_offer.save()
                        continue
                    elif buy_offer.entry_quantity > sale_offer.entry_quantity:
                        try:
                            Trade.objects.create(
                                item_id=buy_offer.item.id,
                                seller=sale_offer.user,
                                buyer=buy_offer.user,
                                quantity=sale_offer.entry_quantity,
                                unit_price=sale_offer.price,
                                seller_offer=sale_offer,
                                buyer_offer=buy_offer,
                                description=f'{buy_offer.user} bought {sale_offer.entry_quantity} shares from \
                                {sale_offer.user} for {sale_offer.price * sale_offer.entry_quantity}'
                            )
                        except IntegrityError:
                            raise (Http404('there is no such user or item'))
                        buy_offer.entry_quantity -= sale_offer.entry_quantity
                        user_inventory.quantity += sale_offer.entry_quantity
                        sale_offer.entry_quantity = 0
                        sale_offer.order_type = 2
                        buy_offer.save()
                        user_inventory.save()
                        sale_offer.save()
                        continue





