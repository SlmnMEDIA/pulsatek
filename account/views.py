from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Sum, Count, Q
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string

from core.decorators import user_is_agen_or_staff, user_is_staff_only

from core.forms import InvitationForm


# INDEX / DASHBOARD VIEW
@login_required(login_url='/login/')
def indexView(request):
    return redirect('account:sale')
    # return render(request, 'account/index_v2.html')


@login_required(login_url='/login/')
@user_is_staff_only
def cartVIew(request):
    return render(request, 'account/cart.html')


# TRANSACTION VIEW
@login_required(login_url='/login/')
def saleView(request):
    return render(request, 'account/trx_v2.html')


# PRODUCT VIEW
@login_required(login_url='/login/')
def productView(request):
    return render(request, 'account/product_v2.html')


# USER VIEW
@login_required(login_url='/login/')
@user_is_agen_or_staff
def memberView(request):
    invite_form = InvitationForm(request.POST or None)
    if request.method == 'POST':
        if invite_form.is_valid():
            instance = invite_form.save(commit=False)
            instance.agen = request.user
            instance.save()
            messages.success(request, 'Invitaion email has been send to {}.'.format(instance.email))
            subject = 'Warungid Invitation Member'
            body = render_to_string(
                'email/email-invitation-body.html',
                {'invit_obj': instance}
            )
            sender = 'support@warungid.com'
            receiver = [instance.email]
            send_mail(subject, body, sender, receiver)
            
    content = {
        'invite_form': invite_form
    }
    return render(request, 'account/member_v2.html', content)


# PAYMENT VIEW
@login_required(login_url='/login/')
@user_is_agen_or_staff
def paymentView(request):
    return render(request, 'account/payment.html')