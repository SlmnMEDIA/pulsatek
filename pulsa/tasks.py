from celery import shared_task
from django.conf import settings
import requests, json, re

import datetime
from django.utils import timezone

from .models import StatusTransaction, ResponseTrx

@shared_task
def pulsa_response_celery(id, payload):
    rjson = dict()
    responsetrx_obj = ResponseTrx.objects.get(pk=id)

    urls = settings.RAJA_URLS

    for url in urls:
        try:
            r = requests.post(url, data=json.dumps(payload), headers={'Content-Type':'application/json'}, verify=False, timeout=5)
            if r.status_code == requests.codes.ok :
                rjson = r.json()
                break

            r.raise_for_status()
        except :
            continue

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

    return '[+] Processing pulsa trx {}'.format(responsetrx_obj.trx.trx_code)



def bulk_update():
    res_objs = ResponseTrx.objects.filter(
        trx__closed=False,
        ref2__isnull=False
    ).exclude(
        ref2__exact=''
    )

    urls = settings.RAJA_URLS
    for res_obj in res_objs:
        h_time = timezone.localtime(res_obj.timestamp) + datetime.timedelta(minutes=1)
        l_time = h_time + datetime.timedelta(days=-1)

        rson = dict()
        
        payload = {
            'method': 'rajabiller.datatransaksi',
            'pin': settings.RAJA_KEY, 
            'uid': settings.RAJA_UID, 
            'id_produk': '', 
            'idpel': '', 
            'tgl1': l_time.strftime('%Y%m%d%H%M%S'), 
            'id_transaksi': '', 
            'tgl2': h_time.strftime('%Y%m%d%H%M%S'), 
            'limit': '', 
        }
        for url in urls:
            try :
                r = requests.post(url, data=json.dumps(payload), verify=False, headers={'Content-Type':'application/json'}, timeout=7)
                if r.status_code == requests.codes.ok:
                    rson = r.json()
                    break

                r.raise_for_status()
            except:
                continue

        data = rson.get('RESULT_TRANSAKSI', [])
        for i in data:
            try :
                code, tgl, prod, prod_name, pel, statcode, stat, price, sn = i.split('#')
                res_trxs = ResponseTrx.objects.filter(ref2=code, trx__closed=False)
                if res_trxs.exists():
                    res_trxs.update(
                        waktu = tgl,
                        no_hp = pel,
                        sn = sn,
                        saldo_terpotong = int(price),
                        status = statcode,
                        ket = stat,
                    )

                    res = res_trxs.get()
                    if res.status=='00':
                        if res.sn != '' and res.sn is not None:
                            StatusTransaction.objects.create(
                                trx = res.trx, status='SS'
                            )
                    elif res.status in ['68','']:
                        pass
                    else :
                        StatusTransaction.objects.create(
                            trx = res.trx, status='FA'
                        )
            except:
                pass