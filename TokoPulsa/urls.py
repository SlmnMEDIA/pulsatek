"""TokoPulsa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

from rest_framework.authtoken import views
from core.views import signupViews
from page.views import home as home_view

urlpatterns = [
    path('', home_view, name='home'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(),{'next_page': '/login/'}, name='logout'),
    path('register/', signupViews, name='signup'),
    path('api-token-auth/', views.obtain_auth_token),
    path('admin/', admin.site.urls),
    path('pulsa/', include('pulsa.urls')),
    path('api/pulsa/', include('pulsa.api.urls')),
    path('game/', include('game.urls')),
    path('api/game/', include('game.api.urls')),
    path('transport/', include('transport.urls')),
    path('api/transport/', include('transport.api.urls')),
    path('account/', include('account.urls')),
    path('sale/', include('sale.urls')),
    path('listrik/', include('listrik.urls')),
    path('core/', include('core.urls')),
    path('api/core/', include('core.api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
