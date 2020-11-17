from django.contrib import admin

from app.models import Trade, Offer, Inventory, Item, WatchList, Price, Currency


class CurrencyAdmin(admin.ModelAdmin):
    fields = ('name', 'code')
    search_fields = ('name',)


class ItemAdmin(admin.ModelAdmin):
    fields = ('price', 'currency', 'details', 'name', 'code')
    search_fields = ('currency',)
    autocomplete_fields = ('currency',)


class WatchListAdmin(admin.ModelAdmin):
    fields = ('user', 'item')
    search_fields = ('user', 'item',)
    autocomplete_fields = ('user', 'item',)


class PriceAdmin(admin.ModelAdmin):
    fields = ('currency', 'price', 'item', 'date')
    search_fields = ('currency', 'item')
    autocomplete_fields = ('currency', 'item')


class OfferAdmin(admin.ModelAdmin):
    fields = ('user', 'item', 'entry_quantity', 'quantity', 'order_type', 'price', 'is_active', 'offer_type')
    search_fields = ('user', 'item',)
    autocomplete_fields = ('user', 'item',)


class TradeAdmin(admin.ModelAdmin):
    fields = ('item', 'buyer', 'seller', 'quantity', 'unit_price', 'description', 'seller_offer', 'buyer_offer')
    search_fields = ('item', 'seller', 'buyer', 'seller_offer', 'buyer_offer')
    autocomplete_fields = ('item', 'seller', 'buyer', 'seller_offer', 'buyer_offer')


class InventoryAdmin(admin.ModelAdmin):
    fields = ('user', 'item', 'quantity')
    search_fields = ('user', 'item',)
    autocomplete_fields = ('user', 'item',)


admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(WatchList, WatchListAdmin)
admin.site.register(Price, PriceAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Trade, TradeAdmin)
admin.site.register(Inventory, InventoryAdmin)
