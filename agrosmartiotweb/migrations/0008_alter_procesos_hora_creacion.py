# Generated by Django 4.2.3 on 2024-07-29 00:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agrosmartiotweb', '0007_delete_sensordata_alter_procesos_hora_creacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='procesos',
            name='hora_creacion',
            field=models.TimeField(default=datetime.time(20, 51, 43, 777263), editable=False),
        ),
    ]
