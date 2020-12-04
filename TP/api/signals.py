from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils import translation
from django.utils.translation import ugettext as _


@receiver(post_save, sender=User)
def my_callback(sender, instance, created, **kwargs):
    if not instance.first_name:
        lang = 'en'
    else:
        lang = instance.first_name
    with translation.override(lang):
        string = _('Hello, we are glad to see you on our website, visit us more often')
    if created and instance.email:
        send_mail(
            'We are happy to welcome you',
            string,
            'texnocd51@gmail.com',
            [instance.email],
        )
