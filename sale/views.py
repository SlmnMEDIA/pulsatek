from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.db.models.functions import TruncDate, TruncMinute
from django.db.models import Count, Sum, Q
from django.template.loader import render_to_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

from .models import Sale, Cash, Payment
from pulsa.models import Product as pulsaProduct
from .forms import AddCashForm
from .tasks import bulk_update_profit
from core.decorators import user_is_agen_or_staff, user_is_staff_only

# DATASET ALL SALE MONTH
@login_required(login_url='/login/')
def chart_data_sale(request):
    data_in_date = dict()
    dataset = Sale.objects.filter(
        type_income='OUT', success=True
    ).annotate(
        date_on=TruncDate('timestamp')
    ).values('date_on').annotate(
        c_trx=Count('id')
    ).values('date_on', 'c_trx').order_by()
    
    for i in dataset :
        data_in_date[i['date_on']] = i['c_trx']

    sort_days = sorted(list(data_in_date.keys()))

    chart = {
        'tooltip': {
            'style': {
                'width': '200px'
            },
            'valueDecimals': 1,
            'shared': True
        },
        'title': {'text': 'Sale Of Month'},
        'rangeSelector': {
            'selected': 0
        },

        'yAxis': {
            'title': {
                'text': ''
            }
        },

        'series': [{
            'name': 'Count TRX',
            'data': list(map(lambda x: [(int(x.strftime('%s'))+25200)*1000, data_in_date[x]], sort_days)),
            'id': 'dataseries'
            },]
    }

    return JsonResponse(chart)



# DATASET BEST PRPDUCT PULSA
@login_required(login_url='/login/')
def chart_pulsa(request):
    data = dict()
    dataset = pulsaProduct.objects.annotate(
        c_prod=Count('transaction', filter=Q(transaction__record__success=True))
    ).values('product_code', 'c_prod')

    for i in dataset :
        data[i['product_code']] = i['c_prod']

    short_prod = sorted(list(map(lambda x: x, data)))

    chart = {
        'chart': {'type': 'column', 'backgroundColor': 'transparent', 'height':300},
        'title': {'text': 'Pulsa & Data'},
        'yAxis': [
            {
                'title': '',
            },
        ],
        'xAxis': {
            'categories': short_prod
        },
        'series': [
            {
                'name': 'Out',
                'data': list(map(lambda x : data[x], short_prod)),
            }
        ]
    }

    return JsonResponse(chart)


# DATA SALE VIEW
# OK
@login_required(login_url='/login/')
def saleListView(request):
    data = dict()
    sale_objs = Sale.objects.filter(
        Q(type_income = 'OUT') & (
            Q(salegame__isnull=False) | Q(salepulsa__isnull=False) | Q(salelistrik__isnull=False) | Q(saletransport__isnull=False)
        )
    )

    # VALIDATION ROLE USER
    if not request.user.is_superuser:
        if request.user.is_agen:
            sale_objs = sale_objs.filter(user__leader=request.user)
        else :
            sale_objs = sale_objs.filter(user=request.user)


    page = request.GET.get('page',1)
    q = request.GET.get('search', None)
    if q:
        sale_objs = sale_objs.filter(
            salepulsa__trx_code__contains=q
        )

    paginator = Paginator(sale_objs, 15)
    try :
        sale_objs = paginator.page(page)
    except PageNotAnInteger:
        sale_objs = paginator.page(1)
    except EmptyPage:
        sale_objs = paginator.page(paginator.num_pages)

    content = {
        'sales': sale_objs
    }
    data['html'] = render_to_string(
        'sale/includes/partial-data-sale.html',
        content,
        request=request
    )
    data['mobile_html'] = render_to_string(
        'sale/includes/partial-data-sale-mobile.html',
        content,
        request=request
    )
    data['html_page'] = render_to_string(
        'sale/includes/partial-page-sale.html',
        content,
        request=request
    )
    return JsonResponse(data)


# DATA SALE PROFIT
# OK
@login_required(login_url='/login/')
def saleProfitView(request):
    data = dict()
    sale_obj = Sale.outcome.all()
    if not request.user.is_superuser :
        if request.user.is_agen:
            sale_obj = sale_obj.filter(
                user__leader = request.user
            )
    profit = sale_obj.profit()
    if not request.user.is_superuser :
        if request.user.is_agen:
            profit = profit * 0.8
        else :
            profit = 0


    data['html'] = render_to_string(
        'sale/includes/partial-profit-value.html',
        {'profit': profit }
    )
    return JsonResponse(data)

    
# FORM ADD CASH
@login_required(login_url='/login/')
@user_is_agen_or_staff
def addCashSaldo(request):
    data = dict()
    form = AddCashForm(request.user ,request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            instance.agen = request.user
            instance.save()

            # temporary func
            cash_obj = Cash.objects.get(pk=instance.id)
            cash_obj.validated = True
            cash_obj.validateby = request.user
            cash_obj.save(update_fields=['validated'])
            data['form_is_valid'] = True
        else :
            data['form_is_valid'] = False

    content = {
        'form': form
    }

    data['html'] = render_to_string(
        'sale/includes/partial-add-cash.html',
        content,
        request=request
    )

    return JsonResponse(data)


# CASH PAYMENT LIST
# OK
@login_required(login_url='/login/')
@user_is_agen_or_staff
def cashListView(request):
    data = dict()
    cash_objs = Cash.objects.all()
    if not request.user.is_superuser:
        if request.user.is_agen:
            cash_objs = cash_objs.filter(user__leader=request.user)

    q = request.GET.get('search', None)
    if q:
        cash_objs = cash_objs.filter(
            nominal=q
        )

    page = request.GET.get('page', 1)
    paginator = Paginator(cash_objs, 20)
    try :
        payment_list = paginator.page(page)
    except PageNotAnInteger:
        payment_list = paginator.page(1)
    except EmptyPage:
        payment_list = paginator.page(paginator.num_pages)
        
    content = {
        'cashs': payment_list
    }

    data['html'] = render_to_string(
        'sale/includes/partial-cash-list.html',
        content,
        request=request
    )
    return JsonResponse(data)


# CASH PAYMENT VALIDATION
# OK
@login_required(login_url='/login/')
@user_is_staff_only
def cashValidationView(request, id):
    data = dict()
    cash_obj = get_object_or_404(Cash, pk=id, delivered=False)
    if request.method == 'POST':
        # cash_obj.validated = True
        # cash_obj.validateby = request.user
        # cash_obj.save(update_fields=['validated'])
        cash_obj.delivered = True
        cash_obj.save()

        cash_objs = Cash.objects.all()
        data['data_html'] = render_to_string(
            'sale/includes/partial-cash-list.html',
            {'cashs': cash_objs },
            request=request
        )

    data['html'] = render_to_string(
        'sale/includes/partial-validate-cash.html',
        {'cash': cash_obj},
        request=request
    )
    return JsonResponse(data)


# PAYMENT LIST
# OK
@login_required(login_url='/login/')
@user_is_staff_only
def paymentListView(request):
    data = dict()
    payment_objs = Payment.objects.all()
    
    q = request.GET.get('search', None)
    if q:
        payment_objs = payment_objs.filter(
            Q(user__first_name__contains=q) | Q(user__email__contains=q)
        )
    page = request.GET.get('page', 1)
    paginator = Paginator(payment_objs, 20)
    try :
        payment_list = paginator.page(page)
    except PageNotAnInteger:
        payment_list = paginator.page(1)
    except EmptyPage:
        payment_list = paginator.page(paginator.num_pages)

    content = {
        'payments': payment_list
    }

    data['html'] = render_to_string(
        'sale/includes/partial-payment-list.html',
        content,
        request=request
    )

    return JsonResponse(data)


# BULK UPDATE PROFIT
def bulkProfitView(request):
    data = dict()
    sale_objs = Sale.objects.filter(
        type_income='OUT',
        success = True,
        closed = False,
        saleprofit = 0,
    )
    if sale_objs.exists():
        bulk_update_profit.delay()

    return JsonResponse(data)

    