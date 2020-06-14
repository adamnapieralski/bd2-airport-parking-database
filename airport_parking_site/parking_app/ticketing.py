from . import models
import os
from django.conf import settings
from django.http import HttpResponse
from django.apps import apps

def get_data():
    strefy_names = []
    strefy = models.Strefa.objects.all()
    for strefa in strefy:
        strefy_names.append(strefa.nazwa)

    return {'strefy_names': strefy_names}