from itertools import chain

from django.db import models
from django.db.models import Max, Q, Count
from app.models import Item


class StatisticManager(models.Manager):
    def most_expensive_item_manager(self):
        return Item.objects.filter(price=Item.objects.aggregate(Max('price'))['price__max']).values()

    def most_popular_manager(self):
        return Item.objects.annotate(
            num_inv=Count('item_inventory', filter=Q(item_inventory__quantity__gt=0))
        ).order_by('-num_inv')[:3].values()


class TestManager(models.Manager):
    def get_queryset(self):
        query = super().get_queryset()
        query1 = query.filter(price=Item.objects.aggregate(Max('price'))['price__max']).values()
        query2 = query.annotate(
            num_inv=Count('item_inventory', filter=Q(item_inventory__quantity__gt=0))
        ).order_by('-num_inv')[:3].values()
        return chain(query1, query2)
