# Generated by Django 4.2.3 on 2024-09-04 23:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agrosmartiotweb', '0002_alter_procesos_hora_creacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='procesos',
            name='hora_creacion',
            field=models.TimeField(default=datetime.time(19, 11, 49, 363288), editable=False),
        ),
    ]
