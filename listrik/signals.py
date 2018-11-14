from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings

import requests, json

from .models import Transaction, ResponseTrx, StatusTransaction
from sale.models import Sale

@receiver(post_save, sender=Transaction)
def sale_listrik_trx(sender, instance, created, **kwargs):
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
            trx = instance
        )

        payload = {
            'method':'rajabiller.inq',
            'uid':settings.RAJA_UID,
            'pin':settings.RAJA_KEY,
            'idpel1':'',
            'idpel2':'',
            'idpel3':'',
            'kode_produk':'PLNPRAH',
            'ref1':instance.trx_code,
        }

        if len(instance.phone) == 11:
            payload['idpel1'] = instance.phone
        elif len(instance.phone) == 12:
            payload['idpel2'] = instance.phone


        rjson = dict()
        urls = settings.RAJA_URLS
        struk = 'Struk kosong.'

        # Send only in production mode
        try:
            r = requests.post(urls[0], data=json.dumps(payload), headers={'Content-Type':'application/json'}, verify=False)
            if r.status_code == requests.codes.ok :
                rjson = r.json()
            r.raise_for_status()
        except :
            pass

        if  rjson.get('STATUS', '99') == '00':
            payload['method'] = 'rajabiller.paydetail'
            payload['ref2'] = rjson['REF2']
            payload['nominal'] = instance.product.nominal
            payload['ref3'] = ''
            
            try:
                r = requests.post(urls[0], data=json.dumps(payload), headers={'Content-Type':'application/json'}, verify=False)
                if r.status_code == requests.codes.ok :
                    rjson = r.json()

                    token = rjson['DETAIL']['TOKEN']
                    kwh = rjson['DETAIL']['PURCHASEDKWHUNIT']
                    struk  = "STRUK PEMBELIAN LISTRIK PRABAYAR\n\nTOKEN : {}\nKWH : {}".format(token, int(kwh)/100)
                r.raise_for_status()
            except :
                pass

        responsetrx_obj.kode_produk = rjson.get('KODE_PRODUK', '')
        responsetrx_obj.waktu = rjson.get('WAKTU', '')
        responsetrx_obj.idpel1 = rjson.get('IDPEL1', '')
        responsetrx_obj.idpel2 = rjson.get('IDPEL2', '')
        responsetrx_obj.idpel3 = rjson.get('IDPEL3', '')
        responsetrx_obj.nama_pelanggan = rjson.get('NAMA_PELANGGAN', '')
        responsetrx_obj.periode = rjson.get('PERIODE', '')
        responsetrx_obj.nominal = rjson.get('NOMINAL', 0)
        responsetrx_obj.admin = rjson.get('ADMIN', 0)
        responsetrx_obj.ref1 = rjson.get('REF1', '')
        responsetrx_obj.ref2 = rjson.get('REF2', '')
        responsetrx_obj.ref3 = rjson.get('REF3', '')
        responsetrx_obj.status = rjson.get('STATUS', '99')
        responsetrx_obj.ket = rjson.get('KET', '')
        responsetrx_obj.saldo_terpotong = rjson.get('SALDO_TERPOTONG', 0)
        responsetrx_obj.sisa_saldo = rjson.get('SISA_SALDO', 0)
        responsetrx_obj.url_struk = rjson.get('URL_STRUK', '')
        responsetrx_obj.datail = struk
        responsetrx_obj.save()


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