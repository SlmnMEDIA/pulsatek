from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http.response import JsonResponse

# Create your views here.

from .models import (
    Product,
    Operator,
    Transaction,
    ResponseTrx,
    StatusTransaction,
)

from .forms import NewTransactionForm
from .tasks import bulk_update

@login_required(login_url='/login/')
def newTrxview(request):
    data = dict()
    form = NewTransactionForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            instance.buyer = request.user
            instance.save()
            return redirect('account:index')

    content = {
        'form': form,
    }
    data['html'] = render_to_string(
        'game/includes/partial-trx-post.html',
        content,
        request=request
    )

    return JsonResponse(data)

@login_required(login_url='/login/')
def productListView(request):
    data = dict()
    operator_objs = Operator.objects.all()

    content = {
        'operators': operator_objs,
    }
    data['html'] = render_to_string(
        'game/includes/partial-product-list.html',
        content,
        request=request
    )
    return JsonResponse(data)


def bulk_updateTransaction(request):
    res_objs = ResponseTrx.objects.filter(
        trx__closed=False
    )
    
    if res_objs.exists():
        bulk_update.delay()
        
    return JsonResponse({'items': res_objs.count()})



