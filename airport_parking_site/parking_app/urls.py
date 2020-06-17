"""airport_parking_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    #path('tickets', views.tickets, name='tickets'),
   # path('reporting', views.reporting, name='reporting'),
  #  path('reporting_download_stats', views.reporting_download_stats, name='reporting_download_stats'),
    path('tickets/<int:id>/', views.make_reservation, name='make_reservation'),
    path('client', views.client_data, name='client_data'),
    path('car/<int:id>/', views.car_data, name='car_data'),
    
]
