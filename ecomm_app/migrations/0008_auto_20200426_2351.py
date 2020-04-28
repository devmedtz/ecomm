# Generated by Django 3.0.4 on 2020-04-26 20:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomm_app', '0007_order_delivered'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='delivered',
        ),
        migrations.RemoveField(
            model_name='order',
            name='delivered_date',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='delivered',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='delivered_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 26, 23, 51, 7, 786827)),
        ),
    ]