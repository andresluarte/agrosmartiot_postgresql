# Generated by Django 4.2.3 on 2024-07-29 00:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agrosmartiotweb', '0006_temperaturehumiditylocation_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SensorData',
        ),
        migrations.AlterField(
            model_name='procesos',
            name='hora_creacion',
            field=models.TimeField(default=datetime.time(20, 47, 50, 518546), editable=False),
        ),
    ]
