from django.urls import path

from . import views

app_name = 'core'
urlpatterns = [
    path('members/', views.userListView, name='member'),
    path('agens/', views.userAgenListView, name='agen_list'),
    path('members/<int:id>/view/', views.userDetailView, name='user-detail'),
    path('members/<int:id>/limit/modify/', views.limitUserModifyView, name='user-limit'),
]