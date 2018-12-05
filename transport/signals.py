from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings

import requests, json

from .models import Transaction, ResponseTrx, StatusTransaction
from sale.models import Sale
from .tasks import transport_response_celery

@receiver(post_save, sender=Transaction)
def sale_transport_trx(sender, instance, created, **kwargs):
    if created:
        StatusTransaction.objects.create(
            trx=instance,
        )

        record_obj = Sale.objects.create(
            user = instance.buyer,
            type_income = 'OUT',
            credit = instance.product.price,
        )

        Transaction.objects.filter(pk=instance.id).update(
            record = record_obj,
            price = instance.product.price,
        )

        responsetrx_obj = ResponseTrx.objects.create(
            trx= instance
        )

        payload = {
            'method':'rajabiller.game',
            'uid':settings.RAJA_UID,
            'pin':settings.RAJA_KEY,
            'no_hp':instance.phone,
            'kode_produk':instance.product.server.code,
            'ref1':instance.trx_code,
        }

        # call celery
        transport_response_celery.delay(responsetrx_obj.id, payload)
        

@receiver(post_save, sender=StatusTransaction)
def status_record_updater(sender, instance, created, **kwargs):
    if created:
        transaction_obj = Transaction.objects.get(statustransaction__id=instance.id)
        # if transaction has failed or canceled by admiin
        if instance.status in ['FA', 'CA']:
            sale_obj = Sale.objects.create(
                user = transaction_obj.buyer,
                type_income = 'IN',
                ref = transaction_obj.record,
                debit = transaction_obj.price
            )

            old_record = transaction_obj.record
            old_record.success = False
            old_record.save()

            transaction_obj.closed = True
            transaction_obj.record = sale_obj
            transaction_obj.save()

        # if transaction success then closed trx
        elif instance.status == 'SS':
            transaction_obj.closed = True
            transaction_obj.save()

        elif instance.status == 'FS':
            sale_obj = Sale.objects.create(
                user = transaction_obj.buyer,
                type_income = 'OUT',
                ref = transaction_obj.record,
                credit = transaction_obj.price
            )
            old_record = transaction_obj.record
            old_record.success = False
            old_record.save()

            transaction_obj.closed = True
            transaction_obj.record = sale_obj
            transaction_obj.save()