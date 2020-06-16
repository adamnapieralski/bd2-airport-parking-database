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
    path('tickets', views.tickets, name='tickets'),
    path('tickets/new/shortterm', views.tickets_new_shortterm, name='tickets_new_shortterm'),
    path('tickets/new/longterm', views.tickets_new_longterm, name='tickets_new_longterm'),
    path('tickets/view/<int:id>', views.tickets_view_id, name='tickets_view_id'),
    path('tickets/view/selected', views.tickets_view_selected, name='tickets_view_selected'),
    path('tickets/pay/<int:id>', views.tickets_pay_id, name='tickets_pay_id'),
    path('tickets/pay/selected', views.tickets_pay_selected, name='tickets_pay_selected'),

]