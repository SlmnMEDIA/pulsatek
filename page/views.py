from django.shortcuts import render, redirect

# Create your views here.


def home(request):
    if request.user.is_authenticated:
        return redirect('account:index')
    return render(request, 'page/home.html')


def noSignUppageView(request):
    return render(request, 'page/no-signup.html')