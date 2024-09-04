from django.db import models
import datetime
from mptt.models import MPTTModel, TreeForeignKey

import re

from django.core.exceptions import ValidationError
# Create yourfrom django.db import models


from mptt.models import MPTTModel, TreeForeignKey

from decimal import Decimal
##validar rut
def validate_rut(value):
    """
    Valida el formato del RUT chileno.
    """
    rut_pattern = r'^\d{1,8}-[\dKk]$'
    if not re.match(rut_pattern, value):
        raise ValidationError('El formato del RUT no es válido')


from django.db import models

class Sector(models.Model):
    nombre = models.CharField(max_length=50)
    latitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    google_maps_link = models.URLField(max_length=200, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.google_maps_link:
            # Extraer coordenadas del enlace de Google Maps
            match = re.search(r'@(-?\d+\.\d+),(-?\d+\.\d+)', self.google_maps_link)
            if match:
                self.latitud = float(match.group(1))
                self.longitud = float(match.group(2))
            else:
                raise ValidationError('El enlace de Google Maps no es válido.')
        super(Sector, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre

class Huerto(MPTTModel):
    nombre = models.CharField(max_length=50)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='lotes')
    

    class MPTTMeta:
        order_insertion_by = ['nombre']

    def __str__(self):
        return self.nombre

class Lote(models.Model):
    nombre = models.CharField(max_length=50)
    huerto = models.ForeignKey(Huerto, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.nombre






class Trabajador(models.Model):
    nombre = models.CharField(max_length=50, null=True)
    rut = models.CharField(max_length=12, null=True, validators=[validate_rut])
    TIPO_CONTRATO_CHOICES = (
        ('Indefinido', 'Indefinido'),
        ('Plazo fijo', 'Plazo fijo'),
        ('Honorario', 'Honorario'),
        ('Sin Contraro', 'Sin Contrato'),
        
    )
   
    fecha_ingreso = models.DateField(default=datetime.date.today)
    fecha_termino_contrato = models.DateField(blank=True, null=True)
    tipo_contraro = models.CharField(max_length=15, choices=TIPO_CONTRATO_CHOICES,default="Plazo fijo", editable=True)
    cobro = models.IntegerField(max_length=10,blank=True,null=True)
    trabajo_a_realizar = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nombre
    @property
    def cantidad_tareas(self):
        return self.procesos_set.count()
    
    @property
    def cantidad_jornada(self):
        return self.jornada_set.count() 
    class Meta:
        ordering = ['-fecha_ingreso',]
   


    

class Procesos(models.Model):
    trabajo = models.CharField(max_length=50, null=True, blank=True)
    fecha = models.DateField(default=datetime.date.today)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, max_length=50, null=True, default="sin especificar",blank=True)
    huerto = models.ForeignKey(Huerto, on_delete=models.CASCADE, max_length=50, null=True, default="sin especificar",blank=True)
    lote= models.ForeignKey(Lote, on_delete=models.CASCADE, max_length=50, null=True, default="sin especificar",blank=True)
    ESTADO_CHOICES = (
        ('Por Realizar', 'Por Realizar'),
        ('En Proceso', 'En Proceso'),
        ('Terminado', 'Terminado'),
    )
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='Por Realizar', editable=True)
    asignado = models.ForeignKey(Trabajador, on_delete=models.CASCADE, max_length=50, null=True)
    hora_asignada = models.TimeField(null=True)
    hora_creacion = models.TimeField(default=datetime.datetime.now().time(),editable=False)
    presupuesto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    observacion = models.CharField(max_length=100, null=True, blank=True)

    


    def __str__(self):
        return self.trabajo
    
class Contacto(models.Model):
    nombre = models.CharField(max_length=50)
    correo = models.EmailField()

    OPCIONES_CONSULTAS = [
        [0,"Consulta"],
        [1,"Reclamo"],
        [2,"Sugerencia"],
        [3,"Felicitaciones"]
    ]
    tipo_consulta = models.IntegerField(choices=OPCIONES_CONSULTAS)
    mensaje = models.TextField()
    avisos = models.BooleanField

    def __str__(self):
        return self.nombre


###sensor
###jornada 


from datetime import date, time, datetime

def current_time():
    return datetime.now().time()

class Jornada(models.Model):
    fecha_creacion = models.DateField(default=date.today, editable=False)
    hora_creacion = models.TimeField(default=current_time, editable=False)
    asignado = models.ForeignKey('Trabajador', on_delete=models.CASCADE, max_length=50, null=True)
    sector = models.ForeignKey('Sector', on_delete=models.CASCADE, max_length=50, null=True, blank=True)
    huerto = models.ForeignKey('Huerto', on_delete=models.CASCADE, max_length=50, null=True, blank=True)
    lote = models.ForeignKey('Lote', on_delete=models.CASCADE, max_length=50, null=True, blank=True)
    fecha = models.DateField()
    ESTADO_CHOICES = (
        ('Por Realizar', 'Por Realizar'),
        ('En Proceso', 'En Proceso'),
        ('Terminado', 'Terminado'),
    )
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='Por Realizar', editable=True)
    
    nombre_tarea_1 = models.CharField(max_length=100)
    hora_inicio_tarea_1 = models.TimeField()
    hora_fin_tarea_1 = models.TimeField()
    cobro_tarea_1 = models.IntegerField(blank=True, null=True)
    
    nombre_tarea_2 = models.CharField(max_length=100, blank=True, null=True)
    hora_inicio_tarea_2 = models.TimeField(blank=True, null=True)
    hora_fin_tarea_2 = models.TimeField(blank=True, null=True)
    cobro_tarea_2 = models.IntegerField(blank=True, null=True)
    
    nombre_tarea_3 = models.CharField(max_length=100, blank=True, null=True)
    hora_inicio_tarea_3 = models.TimeField(blank=True, null=True)
    hora_fin_tarea_3 = models.TimeField(blank=True, null=True)
    cobro_tarea_3 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    nombre_extra_1 = models.CharField(max_length=100, blank=True, null=True)
    gasto_extra_1 = models.IntegerField(blank=True, null=True)

    nombre_extra_2 = models.CharField(max_length=100, blank=True, null=True)
    gasto_extra_2 = models.IntegerField(blank=True, null=True)

    nombre_extra_3 = models.CharField(max_length=100, blank=True, null=True)
    gasto_extra_3 = models.IntegerField(blank=True, null=True)

    observacion = models.CharField(max_length=200, null=True, blank=True)
    total_gasto_jornada = models.IntegerField(blank=True, null=True, editable=False)
    detalle_gasto_total_tareas = models.IntegerField(blank=True, null=True, editable=False)
    detalle_gastos_total_extras = models.IntegerField(blank=True, null=True, editable=False)

    class Meta:
        ordering = ['-fecha_creacion', '-hora_creacion']

    def __str__(self):
        return f"Sector: {self.sector or 'sin especificar'}, Huerto: {self.huerto or 'sin especificar'}, Lote: {self.lote or 'sin especificar'}"

    def save(self, *args, **kwargs):
        self.total_gasto_jornada = self.calcular_gastos_jornada()
        super().save(*args, **kwargs)
        self.actualizar_finanzas()
        self.actualizar_finanzas_por_mes()

    def calcular_gastos_jornada(self):
        total_tareas = sum([
            self.cobro_tarea_1 or 0,
            self.cobro_tarea_2 or 0,
            self.cobro_tarea_3 or 0,
        ])
        total_extras = sum([
            self.gasto_extra_1 or 0,
            self.gasto_extra_2 or 0,
            self.gasto_extra_3 or 0,
        ])
        return total_tareas + total_extras

    def actualizar_finanzas(self):
        if self.estado in ['En Proceso', 'Terminado']:
            trabajador = self.asignado
            finanzas, created = Finanzas.objects.get_or_create(
                trabajador=trabajador,
                trabajo_realiza=trabajador.trabajo_a_realizar,
                cobro_por_hora=trabajador.cobro,
                defaults={
                    'cantidad_jornadas': 0,
                    'horas_trabajadas': Decimal('0.0'),
                    'total_a_pagar': Decimal('0.0'),
                    'estado_pago': 'Por Pagar',
                }
            )
            finanzas.cantidad_jornadas += 1
            horas_trabajadas = Finanzas.calcular_horas_trabajadas(self)
            finanzas.horas_trabajadas += horas_trabajadas
            finanzas.total_a_pagar = finanzas.horas_trabajadas * finanzas.cobro_por_hora
            finanzas.save()

    def actualizar_finanzas_por_mes(self):
        if self.estado in ['En Proceso', 'Terminado']:
            mes = self.fecha.strftime('%B')
            finanzas_por_mes, created = FinanzasPorMes.objects.get_or_create(
                mes=mes,
                defaults={'total_gastos_en_remuneracion': Decimal('0.00')}
            )
            finanzas_por_mes.total_gastos_en_remuneracion += Decimal(str(self.total_gasto_jornada))
            finanzas_por_mes.save()

 


class TemperatureHumidityLocation(models.Model):
    temperature = models.FloatField()
    humidity = models.FloatField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Temperature: {self.temperature}, Humidity: {self.humidity}, Latitude: {self.latitude}, Longitude: {self.longitude}"

class HumiditySoil(models.Model):
    humiditysoil = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Humidity: {self.humiditysoil}, Timestamp: {self.timestamp}"

# temperatura_app/models.py
#treeforeingkey
#MODELO USUARIO

from datetime import date, datetime, timedelta

import calendar
from datetime import datetime, timedelta
from django.utils.translation import activate, get_language
class Finanzas(models.Model):
    ESTADO_PAGO_CHOICES = (
        ('Por Pagar', 'Por Pagar'),
        ('Pagado', 'Pagado'),
    )

    trabajador = models.ForeignKey('Trabajador', on_delete=models.CASCADE)
    trabajo_realiza = models.CharField(max_length=50)
    cobro_por_hora = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_jornadas = models.IntegerField(default=0)
    horas_trabajadas = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total_a_pagar = models.DecimalField(max_digits=10, decimal_places=2, editable=True, default=Decimal('0.00'))
    estado_pago = models.CharField(max_length=10, choices=ESTADO_PAGO_CHOICES, default='Por Pagar', editable=True)

    def __str__(self):
        return f"Finanzas de {self.trabajador.nombre} para el mes de {self.mes}"

    @staticmethod
    def calcular_horas_trabajadas(jornada):
        horas_totales = timedelta()
        for tarea in ['1', '2', '3']:
            hora_inicio = getattr(jornada, f'hora_inicio_tarea_{tarea}')
            hora_fin = getattr(jornada, f'hora_fin_tarea_{tarea}')
            if hora_inicio and hora_fin:
                horas_totales += datetime.combine(date.min, hora_fin) - datetime.combine(date.min, hora_inicio)
        return Decimal(horas_totales.total_seconds() / 3600.0)

    @staticmethod
    def actualizar_finanzas(jornada):
        total_horas_trabajadas = Decimal(Finanzas.calcular_horas_trabajadas(jornada))
        cobro_por_hora = Decimal(jornada.asignado.cobro)
        total_a_pagar = total_horas_trabajadas * cobro_por_hora

        finanzas, creado = Finanzas.objects.get_or_create(
            trabajador=jornada.asignado,
            trabajo_realiza=jornada.nombre_tarea_1,  # O puedes elegir una tarea específica o sumar tareas
            defaults={
                'cobro_por_hora': cobro_por_hora,
                'cantidad_jornadas': 1,
                'horas_trabajadas': total_horas_trabajadas,
                'total_a_pagar': total_a_pagar,
                'estado_pago': 'Por Pagar'
            }
        )

        if not creado:
            finanzas.cobro_por_hora = cobro_por_hora
            finanzas.horas_trabajadas += total_horas_trabajadas
            finanzas.total_a_pagar += total_a_pagar
            finanzas.cantidad_jornadas += 1
            finanzas.save()

from decimal import Decimal
from django.db import models
from decimal import Decimal

class FinanzasPorMes(models.Model):
    mes = models.CharField(max_length=20, unique=True)
    total_gastos_en_remuneracion = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    
    def __str__(self):
        return f"{self.mes} - {self.total_gastos_en_remuneracion}"

class GastoFinancieroManager(models.Manager):
    def gastos_por_mes(self):
        return self.values('mes').annotate(total=models.Sum('monto')).order_by('mes')

class GastoFinanciero(models.Model):
    nombre_gasto = models.CharField(max_length=100)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    fecha_correspondiente = models.DateField()
    mes = models.CharField(max_length=20, editable=False)
    observacion = models.TextField(null=True, blank=True)

    # Configura el Manager personalizado
    objects = GastoFinancieroManager()

    def save(self, *args, **kwargs):
        self.mes = self.fecha_correspondiente.strftime('%B-%Y')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre_gasto} - {self.monto}"

    @staticmethod
    def cantidad_total_gasto_por_mes(mes):
        total = GastoFinanciero.objects.filter(mes=mes).aggregate(total=models.Sum('monto'))['total']
        return total if total is not None else Decimal('0.00')