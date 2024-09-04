# Generated by Django 4.2.3 on 2024-09-04 23:20

import agrosmartiotweb.models
import datetime
from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contacto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('correo', models.EmailField(max_length=254)),
                ('tipo_consulta', models.IntegerField(choices=[[0, 'Consulta'], [1, 'Reclamo'], [2, 'Sugerencia'], [3, 'Felicitaciones']])),
                ('mensaje', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='FinanzasPorMes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mes', models.CharField(max_length=20, unique=True)),
                ('total_gastos_en_remuneracion', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='GastoFinanciero',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_gasto', models.CharField(max_length=100)),
                ('monto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fecha_ingreso', models.DateTimeField(auto_now_add=True)),
                ('fecha_correspondiente', models.DateField()),
                ('mes', models.CharField(editable=False, max_length=20)),
                ('observacion', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Huerto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lotes', to='agrosmartiotweb.huerto')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HumiditySoil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('humiditysoil', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Lote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('huerto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agrosmartiotweb.huerto')),
            ],
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('latitud', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('longitud', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('google_maps_link', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TemperatureHumidityLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temperature', models.FloatField()),
                ('humidity', models.FloatField()),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Trabajador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, null=True)),
                ('rut', models.CharField(max_length=12, null=True, validators=[agrosmartiotweb.models.validate_rut])),
                ('fecha_ingreso', models.DateField(default=datetime.date.today)),
                ('fecha_termino_contrato', models.DateField(blank=True, null=True)),
                ('tipo_contraro', models.CharField(choices=[('Indefinido', 'Indefinido'), ('Plazo fijo', 'Plazo fijo'), ('Honorario', 'Honorario'), ('Sin Contraro', 'Sin Contrato')], default='Plazo fijo', max_length=15)),
                ('cobro', models.IntegerField(blank=True, max_length=10, null=True)),
                ('trabajo_a_realizar', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ['-fecha_ingreso'],
            },
        ),
        migrations.CreateModel(
            name='Procesos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trabajo', models.CharField(blank=True, max_length=50, null=True)),
                ('fecha', models.DateField(default=datetime.date.today)),
                ('estado', models.CharField(choices=[('Por Realizar', 'Por Realizar'), ('En Proceso', 'En Proceso'), ('Terminado', 'Terminado')], default='Por Realizar', max_length=15)),
                ('hora_asignada', models.TimeField(null=True)),
                ('hora_creacion', models.TimeField(default=datetime.time(19, 20, 3, 921749), editable=False)),
                ('presupuesto', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('observacion', models.CharField(blank=True, max_length=100, null=True)),
                ('asignado', models.ForeignKey(max_length=50, null=True, on_delete=django.db.models.deletion.CASCADE, to='agrosmartiotweb.trabajador')),
                ('huerto', models.ForeignKey(blank=True, default='sin especificar', max_length=50, null=True, on_delete=django.db.models.deletion.CASCADE, to='agrosmartiotweb.huerto')),
                ('lote', models.ForeignKey(blank=True, default='sin especificar', max_length=50, null=True, on_delete=django.db.models.deletion.CASCADE, to='agrosmartiotweb.lote')),
                ('sector', models.ForeignKey(blank=True, default='sin especificar', max_length=50, null=True, on_delete=django.db.models.deletion.CASCADE, to='agrosmartiotweb.sector')),
            ],
        ),
        migrations.CreateModel(
            name='Jornada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creacion', models.DateField(default=datetime.date.today, editable=False)),
                ('hora_creacion', models.TimeField(default=agrosmartiotweb.models.current_time, editable=False)),
                ('fecha', models.DateField()),
                ('estado', models.CharField(choices=[('Por Realizar', 'Por Realizar'), ('En Proceso', 'En Proceso'), ('Terminado', 'Terminado')], default='Por Realizar', max_length=15)),
                ('nombre_tarea_1', models.CharField(max_length=100)),
                ('hora_inicio_tarea_1', models.TimeField()),
                ('hora_fin_tarea_1', models.TimeField()),
                ('cobro_tarea_1', models.IntegerField(blank=True, null=True)),
                ('nombre_tarea_2', models.CharField(blank=True, max_length=100, null=True)),
                ('hora_inicio_tarea_2', models.TimeField(blank=True, null=True)),
                ('hora_fin_tarea_2', models.TimeField(blank=True, null=True)),
                ('cobro_tarea_2', models.IntegerField(blank=True, null=True)),
                ('nombre_tarea_3', models.CharField(blank=True, max_length=100, null=True)),
                ('hora_inicio_tarea_3', models.TimeField(blank=True, null=True)),
                ('hora_fin_tarea_3', models.TimeField(blank=True, null=True)),
                ('cobro_tarea_3', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('nombre_extra_1', models.CharField(blank=True, max_length=100, null=True)),
                ('gasto_extra_1', models.IntegerField(blank=True, null=True)),
                ('nombre_extra_2', models.CharField(blank=True, max_length=100, null=True)),
                ('gasto_extra_2', models.IntegerField(blank=True, null=True)),
                ('nombre_extra_3', models.CharField(blank=True, max_length=100, null=True)),
                ('gasto_extra_3', models.IntegerField(blank=True, null=True)),
                ('observacion', models.CharField(blank=True, max_length=200, null=True)),
                ('total_gasto_jornada', models.IntegerField(blank=True, editable=False, null=True)),
                ('detalle_gasto_total_tareas', models.IntegerField(blank=True, editable=False, null=True)),
                ('detalle_gastos_total_extras', models.IntegerField(blank=True, editable=False, null=True)),
                ('asignado', models.ForeignKey(max_length=50, null=True, on_delete=django.db.models.deletion.CASCADE, to='agrosmartiotweb.trabajador')),
                ('huerto', models.ForeignKey(blank=True, max_length=50, null=True, on_delete=django.db.models.deletion.CASCADE, to='agrosmartiotweb.huerto')),
                ('lote', models.ForeignKey(blank=True, max_length=50, null=True, on_delete=django.db.models.deletion.CASCADE, to='agrosmartiotweb.lote')),
                ('sector', models.ForeignKey(blank=True, max_length=50, null=True, on_delete=django.db.models.deletion.CASCADE, to='agrosmartiotweb.sector')),
            ],
            options={
                'ordering': ['-fecha_creacion', '-hora_creacion'],
            },
        ),
        migrations.AddField(
            model_name='huerto',
            name='sector',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agrosmartiotweb.sector'),
        ),
        migrations.CreateModel(
            name='Finanzas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trabajo_realiza', models.CharField(max_length=50)),
                ('cobro_por_hora', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cantidad_jornadas', models.IntegerField(default=0)),
                ('horas_trabajadas', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10)),
                ('total_a_pagar', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10)),
                ('estado_pago', models.CharField(choices=[('Por Pagar', 'Por Pagar'), ('Pagado', 'Pagado')], default='Por Pagar', max_length=10)),
                ('trabajador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agrosmartiotweb.trabajador')),
            ],
        ),
    ]
