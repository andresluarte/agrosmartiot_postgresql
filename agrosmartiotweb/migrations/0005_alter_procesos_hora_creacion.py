# Generated by Django 4.2.3 on 2024-07-11 10:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agrosmartiotweb', '0004_alter_procesos_hora_creacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='procesos',
            name='hora_creacion',
            field=models.TimeField(default=datetime.time(6, 4, 13, 999966), editable=False),
        ),
    ]
