from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.core.mail import send_mail


@receiver(post_save, sender=User)
def my_callback(sender, instance,  created,  **kwargs):
    if created and instance.email:
        send_mail(
            'We are happy to welcome you',
            'Hello, we are glad to see you on our website, visit us more often',
            'texnocd51@gmail.com',
            [instance.email],
        )
