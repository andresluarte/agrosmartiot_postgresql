# Generated by Django 4.2.3 on 2024-09-04 23:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agrosmartiotweb', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='procesos',
            name='hora_creacion',
            field=models.TimeField(default=datetime.time(19, 23, 34, 297358), editable=False),
        ),
    ]