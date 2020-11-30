from django.db.models import Max
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from app.models import Inventory, Item


@receiver(post_save, sender=User)
def my_callback(sender, instance,  created,  **kwargs):
    if created:
        try:
            Inventory.objects.create(
                user=instance,
                item=Item.objects.filter(price=Item.objects.aggregate(Max('price'))['price__max'])[0],
            )
        except:
            pass
