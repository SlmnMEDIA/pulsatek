from celery import shared_task
from django.conf import settings

import requests, json
from .models import StatusTransaction, ResponseTrx

@shared_task
def listrik_response_celery(id, payload):
    responsetrx_obj = ResponseTrx.objects.get(pk=id)
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
        payload['nominal'] = responsetrx_obj.trx.product.nominal
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