from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings

import requests, json

from .models import Transaction, ResponseTrx, StatusTransaction
from sale.models import Sale

@receiver(post_save, sender=Transaction)
def sale_game_trx(sender, instance, created, **kwargs):
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

        rjson = dict()
        urls = settings.RAJA_URLS

        # Send only in production mode
        try:
            r = requests.post(urls[0], data=json.dumps(payload), headers={'Content-Type':'application/json'}, verify=False)
            if r.status_code == requests.codes.ok :
                rjson = r.json()
            r.raise_for_status()
        except :
            pass

        responsetrx_obj.kode_produk = rjson.get('KODE_PRODUK', '')
        responsetrx_obj.waktu = rjson.get('WAKTU', '')
        responsetrx_obj.no_hp = rjson.get('NO_HP', '')
        responsetrx_obj.sn = rjson.get('SN', '')
        responsetrx_obj.ref1 = rjson.get('REF1', '')
        responsetrx_obj.ref2 = rjson.get('REF2', '')
        responsetrx_obj.status = rjson.get('STATUS', '99')
        responsetrx_obj.ket = rjson.get('KET', 'Gagal terhubung ke server / timeout')
        responsetrx_obj.saldo_terpotong = int(rjson.get('SALDO_TERPOTONG', 0))
        responsetrx_obj.sisa_saldo = int(rjson.get('SISA_SALDO', 0))
        responsetrx_obj.save()

        if responsetrx_obj.status == '99':
            StatusTransaction.objects.create(trx=instance, status='FA')


@receiver(post_save, sender=StatusTransaction)
def status_record_updater(sender, instance, created, **kwargs):
    if created:
        transaction_obj = Transaction.objects.get(statustransaction__id=instance.id)
        # if transaction has failed or canceled by admiin
        if instance.status in ['FA', 'CA']:
            Sale.objects.create(
                user = transaction_obj.buyer,
                type_income = 'IN',
                ref = transaction_obj.record,
                debit = transaction_obj.price
            )
            transaction_obj.closed = True
            transaction_obj.save()

            transaction_obj.record.success = False
            transaction_obj.record.save()

        # if transaction success then closed trx
        elif instance.status == 'SS':
            transaction_obj.closed = True
            transaction_obj.save()