from django.db import models
import datetime
from mptt.models import MPTTModel, TreeForeignKey

import re

from django.core.exceptions import ValidationError
# Create yourfrom django.db import models

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


##validar rut
def validate_rut(value):
    """
    Valida el formato del RUT chileno.
    """
    rut_pattern = r'^\d{1,8}-[\dKk]$'
    if not re.match(rut_pattern, value):
        raise ValidationError('El formato del RUT no es válido')

class Sector(models.Model):
    nombre = models.CharField(max_length=50)
    

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


class SensorData(models.Model):
    temperature = models.FloatField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.temperature



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




class Jornada(models.Model):
    fecha_creacion = models.DateField(default=datetime.date.today,editable=False)
    hora_creacion = models.TimeField(default=datetime.datetime.now().time(),editable=False)

    asignado = models.ForeignKey(Trabajador, on_delete=models.CASCADE, max_length=50, null=True)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, max_length=50, null=True, blank=True)
    huerto = models.ForeignKey(Huerto, on_delete=models.CASCADE, max_length=50, null=True ,blank=True)
    lote= models.ForeignKey(Lote, on_delete=models.CASCADE, max_length=50, null=True, blank=True)
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
    cobro_tarea_1 = models.IntegerField(max_length=10,blank=True,null=True)
    
    nombre_tarea_2 = models.CharField(max_length=100, blank=True, null=True)
    hora_inicio_tarea_2 = models.TimeField(blank=True, null=True)
    hora_fin_tarea_2 = models.TimeField(blank=True, null=True)
    cobro_tarea_2 = models.IntegerField(max_length=10,blank=True,null=True)
    

    nombre_tarea_3 = models.CharField(max_length=100, blank=True, null=True)
    hora_inicio_tarea_3 = models.TimeField(blank=True, null=True)
    hora_fin_tarea_3 = models.TimeField(blank=True, null=True)
    cobro_tarea_3 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    ##ccampos extra 1
    nombre_extra_1 = models.CharField(max_length=100, blank=True, null=True)
    gasto_extra_1 = models.IntegerField(max_length=10,blank=True,null=True)

    #campos extra 2
    nombre_extra_2 = models.CharField(max_length=100, blank=True, null=True)
    gasto_extra_2 = models.IntegerField(max_length=10,blank=True,null=True)

    #campos extra 3 
    nombre_extra_3 = models.CharField(max_length=100, blank=True, null=True)
    gasto_extra_3 = models.IntegerField(max_length=10,blank=True,null=True)

    observacion = models.CharField(max_length=200, null=True, blank=True)
    total_gasto_jornada = models.IntegerField(max_length=10,blank=True,null=True,editable=False)
    detalle_gasto_total_tareas = models.IntegerField(max_length=10,blank=True,null=True,editable=False)
    detalle_gastos_total_extras = models.IntegerField(max_length=10,blank=True,null=True,editable=False)

    class Meta:
        ordering = ['-fecha_creacion','-hora_creacion']








    def __str__(self):
        return f"Sector: {self.sector or 'sin especificar'}, Huerto: {self.huerto or 'sin especificar'}, Lote: {self.lote or 'sin especificar'}"
 
class TemperatureHumidity(models.Model):
    temperature = models.FloatField()
    humidity = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
# temperatura_app/models.py
#treeforeingkey
#MODELO USUARIO





   


