from django.dispatch import receiver
from django.conf import settings
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.template.loader import render_to_string


from rest_framework.authtoken.models import Token


# Token Generate Instance
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def generate_token(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)
        if instance.leader is None:
            instance.leader = instance
            instance.save()

        subject = 'Registrasi Member Warungid'
        body = render_to_string(
            'email/register-email.html',
            {'newuser': instance}
        )
        sender = 'support@warungid.com'
        receiver = [instance.email]
        send_mail(subject, body, sender, receiver)