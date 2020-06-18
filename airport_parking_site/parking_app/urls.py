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
    path('tickets/', views.tickets, name='parking_app-tickets'),
    path('tickets/new/shortterm/', views.tickets_new_shortterm, name='tickets_new_shortterm'),
    path('tickets/new/longterm/', views.tickets_new_longterm, name='tickets_new_longterm'),
    path('tickets/view/<int:id>/', views.tickets_view_id, name='tickets_view_id'),
    path('tickets/view/selected/', views.tickets_view_selected, name='tickets_view_selected'),
    path('tickets/pay/<int:id>/', views.tickets_pay_id, name='tickets_pay_id'),
    path('tickets/pay/selected/', views.tickets_pay_selected, name='tickets_pay_selected'),
    path('resv/', views.reservation, name='parking_app-resv'),
    path('report/', views.reporting, name='parking_app-report'),
    path('report_download_stats', views.reporting_download_stats, name='parking_app-reporting_download_stats'),
    path('report_download_data', views.reporting_download_data, name='parking_app-reporting_download_data'),
    path('reservation/', views.make_reservation, name='make_reservation'),
    path('client', views.client_data, name='client_data'),
    path('car/<int:id>/', views.car_data, name='car_data'),
    path('profile/<int:id>/myreservations', views.see_reservations, name='see_reservations'), 
    path('test_myreservations', views.test_myreservations, name='test_myreservations'),
]
