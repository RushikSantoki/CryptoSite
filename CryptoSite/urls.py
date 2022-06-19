"""CryptoSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from CryptoSite import views

app_name = 'CryptoSite'
urlpatterns = [
    path('', views.welcomePage, name='welcome'),
    path('admin/', admin.site.urls),
    path('about/', views.aboutPage, name='about'),
    path('signin/', views.signInPage, name='signIn'),
    path('signup/', views.signUpPage, name='signUp'),
    path('mainpage/', views.mainPage, name='mainPage'),
    path('detail/<int:rank>/', views.detailPage, name='rank'),
    path('buy/<int:curr_rank>/', views.buyPage, name='buy'),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('confirm/<int:rank>/<str:coins>', views.confirm, name='confirm'),
    path('success/<int:rank>/<str:coins>', views.success, name='success'),
    path('profile/', views.profile, name='profile')
]
