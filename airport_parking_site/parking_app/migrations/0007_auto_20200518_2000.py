# Generated by Django 3.0.3 on 2020-05-18 20:00

from django.db import migrations
import dane.initial_migration as im

class Migration(migrations.Migration):

    dependencies = [
        ('parking_app', '0006_auto_20200518_1647'),
    ]

    operations = [
        migrations.RunPython(im.initial_migration)
    ]
