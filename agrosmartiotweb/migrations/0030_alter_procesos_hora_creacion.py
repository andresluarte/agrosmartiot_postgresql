# Generated by Django 4.2.3 on 2023-09-26 22:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agrosmartiotweb', '0029_alter_jornada_huerto_alter_jornada_lote_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='procesos',
            name='hora_creacion',
            field=models.TimeField(default=datetime.time(19, 33, 3, 564682), editable=False),
        ),
    ]