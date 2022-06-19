from django.contrib import admin
from django.urls import path, include
from CryptoSite import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('CryptoSite.urls'))
]
