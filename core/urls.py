from django.urls import path

from . import views

app_name = 'core'
urlpatterns = [
    path('members/', views.userListView, name='member'),
    path('members/create/', views.addMemberView, name='create_member'),
    path('agens/', views.userAgenListView, name='agen_list'),
    path('message/', views.messageListView, name='message_list'),
    path('message/post/', views.messagePostView, name='message_post'),
    path('members/<int:id>/view/', views.userDetailView, name='user-detail'),
    path('members/<int:id>/limit/modify/', views.limitUserModifyView, name='user-limit'),
]