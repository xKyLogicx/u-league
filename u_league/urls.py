"""
URL configuration for u_league project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tim/', include('manage_tim.urls')),
    path('mulai-rapat/', include('mulai_rapat.urls')),
    path('', include ('authentication.urls')),
    path('crud_pertandingan/', include('crud_pertandingan.urls')),
    path('cru_peminjamanstadium/', include('cru_peminjamanstadium.urls')),
    path('manager/', include('manager.urls')),
    path('penonton/', include('penonton.urls')),
    path('panitia/', include('panitia.urls')),
]
