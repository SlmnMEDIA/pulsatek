from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Count, Q, Sum

from .forms import SignUpForm, LimitUserForm, InvitationForm
from .decorators import user_is_agen_or_staff, user_is_referal_agen, user_is_staff_only
from core.models import Invitation

User_class = get_user_model()

# SIGNUP VIEW
def signupViews(request):
    ref = request.GET.get('r', None)
    try :
        invit_obj = Invitation.objects.get(code=ref, closed=False)
        form = SignUpForm(ref ,request.POST or None, initial={'email': invit_obj.email})
    except:
        form = SignUpForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            try :
                instance = form.save(commit=False)
                instance.leader = invit_obj.agen
                instance.save()
                invit_obj.closed = True
                invit_obj.save()
            except:
                form.save()

            return redirect('account:index')

    content = {
        'form': form,
    }
    return render(request, 'core/signup.html', content)


# USER LIST
# OK
@login_required(login_url='/login/')
@user_is_agen_or_staff
def userListView(request):
    data = dict()
    user_objs = User_class.objects.annotate(
        user_c = Count('sale', filter=Q(sale__type_income='OUT'))
    )

    if not request.user.is_superuser:
        if request.user.is_agen:
            user_objs = user_objs.filter(leader=request.user)

    q = request.GET.get('search', None)
    if q :
        user_objs = user_objs.filter(email__contains=q)

    content = {
        'members': user_objs
    }

    data['html'] = render_to_string(
        'core/includes/partial-user-list.html',
        content,
        request=request
    )
    return JsonResponse(data)


@login_required
@user_is_staff_only
def userAgenListView(request):
    data = dict()
    user_objs = User_class.objects.filter(
        is_agen=True
    ).annotate(
        c_member = Count('user')
    )

    content = {
        'agens': user_objs
    }

    data['html'] = render_to_string(
        'core/includes/partial-agen-list.html',
        content,
        request=request
    )
    return JsonResponse(data)


# USER DETAIL
@login_required(login_url='/login/')
def userDetailView(request, id):
    user_obj = get_object_or_404(User_class, pk=id)
    data = dict()

    content = {
        'member': user_obj,
    }

    data['html'] = render_to_string(
        'core/includes/partial-detail-user.html',
        content,
        request=request
    )
    return JsonResponse(data)


# MODIFY LIMIT
# OK
@login_required(login_url='/login/')
@user_is_agen_or_staff
@user_is_referal_agen
def limitUserModifyView(request, id):
    user_obj = get_object_or_404(User_class, pk=id)
    data = dict()

    form = LimitUserForm(request.user, request.POST or None, instance=user_obj)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            members = User_class.objects.annotate(
                user_c = Count('sale', filter=Q(sale__type_income='OUT'))
            )
            if not request.user.is_superuser:
                if request.user.is_agen:
                    members = members.filter(leader=request.user)

            data['html_data'] = render_to_string(
                'core/includes/partial-user-list.html',
                {'members':members},
                request=request
            )
        else :
            data['form_is_valid'] = False

    content = {
        'form': form,
        'member': user_obj
    }
    
    data['html'] = render_to_string(
        'core/includes/partial-limit-form.html',
        content,
        request=request
    )
    return JsonResponse(data)
