from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models import F
from django.contrib.auth import get_user_model

from .models import Sale, Payment, Cash

@receiver(post_save, sender=Sale)
def define_balance_record(sender, instance, created, **kwargs):
    if created:
        # Balance saldo
        Sale.objects.filter(pk=instance.id).update(
            balance = instance.user_balance() - F('credit') + F('debit')
        )

        instance.refresh_from_db()
        # New saldo user
        user_obj = get_user_model()
        user_obj.objects.filter(pk=instance.user_id).update(
            saldo = instance.balance
        )

@receiver(post_save, sender=Payment)
def payment_process(sender, instance, created, **kwargs):
    if created:
        Sale.objects.create(
            type_income='IN',
            debit = instance.nominal,
            user = instance.user
        )


@receiver(post_save, sender=Cash)
def cash_income(sender, instance, created, update_fields, **kwargs):
    if update_fields is not None:
        if 'validated' in update_fields:
            if instance.validated == True:
                pay_obj = Payment.objects.create(
                    nominal = instance.nominal,
                    user = instance.user,
                )

                instance.payment = pay_obj
                instance.save()