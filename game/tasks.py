from celery import shared_task
from django.conf import settings

import requests, json
from .models import StatusTransaction, ResponseTrx

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
                                else :
                                    StatusTransaction.objects.create(
                                        trx = res.trx, status='FA'
                                    )
                except:
                    pass

    return '{} transaction object has updated!'.format(res_objs.count())