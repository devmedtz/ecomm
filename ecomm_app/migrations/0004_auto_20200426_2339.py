# Generated by Django 3.0.4 on 2020-04-26 20:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomm_app', '0003_auto_20200417_1754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivered_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 26, 23, 39, 16, 1612)),
        ),
    ]
