from celery import shared_task
from django.conf import settings

import requests, json
from .models import StatusTransaction, ResponseTrx

@shared_task
def game_response_celery(id, payload):
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

    return '[+] Processing game trx {}'.format(responsetrx_obj.trx.trx_code)
    

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
    urls = settings.RAJA_URLS
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


                for url in urls:                
                    try :
                        r = requests.post(url, data=json.dumps(payload), verify=False, headers={'Content-Type':'application/json'}, timeout=5)
                        if r.status_code == requests.codes.ok:
                            try :
                                rjson = r.json()
                                if rjson['STATUS'] == '00':
                                    result = rjson['RESULT_TRANSAKSI'][0]
                                    code, tgl, prod, prod_name, pel, statcode, stat, price, sn = result.split('#')
                                    res.sn = sn
                                    res.saldo_terpotong = int(price)
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

                            finally:
                                break

                        r.raise_for_status()
                    except:
                        continue

    return '[?] {} transaction game has updated!'.format(res_objs.count())