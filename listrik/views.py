from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http.response import JsonResponse

# Create your views here.

from .models import (
    Product,
    Operator,
)

from .forms import NewTransactionForm

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
        'listrik/includes/partial-trx-post.html',
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
        'listrik/includes/partial-product-list.html',
        content,
        request=request
    )
    return JsonResponse(data)