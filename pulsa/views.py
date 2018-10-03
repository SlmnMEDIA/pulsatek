from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http.response import JsonResponse

# Create your views here.

from .models import (
    Product,
    Operator, PrefixNumber
)

from .forms import NewProductForm, NewTransactionForm

# POSTING NEW TRX
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
        'pulsa/includes/partial-trx-post.html',
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
        'pulsa/includes/partial-product-list.html',
        content,
        request=request
    )
    return JsonResponse(data)

@login_required(login_url='/login/')
def productDataList(request):
    data = dict()
    operator_objs = Operator.objects.all()

    content = {
        'operators': operator_objs,
    }
    data['html'] = render_to_string(
        'pulsa/includes/partial-product-data-list.html',
        content,
        request=request
    )
    return JsonResponse(data)


@login_required(login_url='/login/')
def addproductView(request):
    data = dict()
    form = NewProductForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            product_objs = Product.objects.all()

            data['data_list'] = render_to_string(
                'pulsa/includes/partial-product-list.html',
                {'products': product_objs },
                request=request
            )
        else :
            data['form_is_valid'] = False
    
    content = {
        'form': form
    }
    data['html'] = render_to_string(
        'pulsa/includes/partial-add-product.html',
        content,
        request=request
    )

    return JsonResponse(data)

# @login_required
# def updateproductView(request, id):
#     data = dict()
#     product_obj = get_object_or_404(Product, pk=id)
#     form = NewProductForm(request.POST or None, instance=product_obj)
#     if request.method == 'POST':
#         if form.is_valid():
#             form.save()
#             data['form_is_valid'] = True
#             product_objs = Product.objects.all()

#             data['data_list'] = render_to_string(
#                 'pulsa/includes/partial-product-list.html',
#                 {'products': product_objs },
#                 request=request
#             )
#         else :
#             data['form_is_valid'] = False

#     content = {
#         'form': form
#     }
#     data['html'] = render_to_string(
#         'pulsa/includes/partial-add-product.html',
#         content,
#         request=request
#     )

#     return JsonResponse(data)