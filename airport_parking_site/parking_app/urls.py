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
    path('', views.home, name='parking_app-home'),    
    path('ticket/', views.ticket, name='parking_app-ticket'),
    path('resv/', views.reservation, name='parking_app-resv'),
    path('report/', views.reporting, name='parking_app-report'),
    path('report_download_stats', views.reporting_download_stats, name='parking_app-reporting_download_stats'),
    path('report_download_data', views.reporting_download_data, name='parking_app-reporting_download_data'),
]
