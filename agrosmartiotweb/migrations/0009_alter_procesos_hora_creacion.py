# Generated by Django 4.2.3 on 2024-07-11 10:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agrosmartiotweb', '0008_alter_procesos_hora_creacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='procesos',
            name='hora_creacion',
            field=models.TimeField(default=datetime.time(6, 44, 39, 255370), editable=False),
        ),
    ]
