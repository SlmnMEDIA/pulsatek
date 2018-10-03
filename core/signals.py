from django.dispatch import receiver
from django.conf import settings
from django.db.models.signals import post_save

from rest_framework.authtoken.models import Token

# Token Generate Instance
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def generate_token(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)
        instance.leader = instance
        instance.save()