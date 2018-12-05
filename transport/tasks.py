from celery import shared_task
from django.conf import settings

import requests, json
from .models import StatusTransaction, ResponseTrx

@shared_task
def transport_response_celery(id, payload):
    rjson = dict()
    responsetrx_obj = ResponseTrx.objects.get(pk=id)

    urls = settings.RAJA_URLS

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

@shared_task
def bulk_update():
    res_objs = ResponseTrx.objects.filter(
        trx__closed=False
    )
    payload = {
        'method': 'rajabiller.datatransaksi',
        'pin': settings.RAJA_KEY, 
        'uid': settings.RAJA_UID, 
        'id_produk': '', 
        'idpel': '', 
        'tgl1': '', 
        'id_transaksi': '', 
        'tgl2': '', 
        'limit': '', 
    }
    url = settings.RAJA_URLS
    for res in res_objs:
        if res.status == '00' and res.sn != '' and res.sn is not None:
            StatusTransaction.objects.create(
                trx = res.trx, status='SS'
            )
        else :
            if res.ref1 is not None and res.ref1 !='':
                payload['tgl1'] = res.waktu
                payload['tgl2'] = res.waktu
                payload['id_transaksi'] = res.ref2

                try :
                    r = requests.post(url[0], data=json.dumps(payload), verify=False, headers={'Content-Type':'application/json'})
                    if r.status_code == requests.codes.ok:
                        rjson = r.json()
                        if rjson['STATUS'] == '00':
                            result = rjson['RESULT_TRANSAKSI'][0]
                            code, tgl, prod, prod_name, pel, statcode, stat, price, sn = result.split('#')
                            res.sn = sn
                            res.price = int(price)
                            res.status = statcode
                            res.ket = stat
                            res.save()
                            if res.status is not None and res.status != '':
                                if res.status=='00':
                                    if res.sn != '' and res.sn is not None:
                                        StatusTransaction.objects.create(
                                            trx = res.trx, status='SS'
                                        )
                                elif res.status=='68':
                                    pass
                                else :
                                    StatusTransaction.objects.create(
                                        trx = res.trx, status='FA'
                                    )
                except:
                    pass

    return '{} transaction object has updated!'.format(res_objs.count())