# Generated by Django 3.0.3 on 2020-06-16 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking_app', '0005_auto_20200616_1115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bilet',
            name='nr_biletu',
            field=models.IntegerField(),
        ),
    ]
