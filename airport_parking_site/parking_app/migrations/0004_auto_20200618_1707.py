# Generated by Django 3.0.5 on 2020-06-18 17:07

from django.db import migrations
import dane.tests_data_migration as tdm


class Migration(migrations.Migration):

    dependencies = [
        ('parking_app', '0003_auto_20200618_1706'),
    ]

    operations = [
        migrations.RunPython(tdm.update_strefa)
    ]
