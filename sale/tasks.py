from celery import shared_task
from django.conf import settings

import requests, json
from .models import Sale

@shared_task
def bulk_update_profit():
    sale_objs = Sale.objects.filter(
        type_income='OUT',
        success = True,
        closed = False,
        saleprofit = 0,
    )
    for sale_obj in sale_objs:
        sale_obj.saleprofit = sale_obj.profit()
        sale_obj.save(update_fields=['saleprofit'])

    return 'Update {} profits'.format(sale_objs.count())
    