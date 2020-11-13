from django.contrib import admin

from app.models import Trade, Offer, Inventory, Item, WatchList, Price, Currency


class CurrencyAdmin(admin.ModelAdmin):
    fields = ('name', 'code')


class ItemAdmin(admin.ModelAdmin):
    fields = ('price', 'currency', 'details', 'name', 'code')


class WatchListAdmin(admin.ModelAdmin):
    fields = ('user', 'item')


class PriceAdmin(admin.ModelAdmin):
    fields = ('currency', 'price', 'item', 'date')


class OfferAdmin(admin.ModelAdmin):
    fields = ('user', 'item', 'entry_quantity', 'quantity', 'order_type', 'price', 'is_active', 'offer_type')


class TradeAdmin(admin.ModelAdmin):
    fields = ('item', 'seller', 'quantity', 'unit_price', 'description', 'seller_offer', 'buyer_offer')


class InventoryAdmin(admin.ModelAdmin):
    fields = ('user', 'item', 'quantity')


admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(WatchList, WatchListAdmin)
admin.site.register(Price, PriceAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Trade, TradeAdmin)
admin.site.register(Inventory, InventoryAdmin)
