from django.urls import path

from . import views

app_name = 'page'
urlpatterns = [
    path('home/', views.home, name='home'),
    path('signup-unpage/', views.noSignUppageView, name='no_signup'),
]