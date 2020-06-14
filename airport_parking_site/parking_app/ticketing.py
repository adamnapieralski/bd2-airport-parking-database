from . import models
import os
from django.conf import settings
from django.http import HttpResponse
from django.apps import apps

def get_data(table):
    models_names = []
    models_list = apps.get_app_config('parking_app').get_models()
    for model in models_list:
        models_names.append(model._meta.db_table.replace('parking_app_', ''))

    return {'tables': models_names}