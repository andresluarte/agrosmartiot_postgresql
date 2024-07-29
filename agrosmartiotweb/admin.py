from django.contrib import admin
from import_export import resources
from .models import Procesos,Contacto,Trabajador,Jornada,Sector,Huerto,Lote
from import_export.fields import Field


admin.site.register(Procesos)

admin.site.register(Contacto)
admin.site.register(Trabajador)
admin.site.register(Jornada)

admin.site.register(Sector)
admin.site.register(Huerto)
admin.site.register(Lote)
class ProcesosResource(resources.ModelResource):
    sector_nombre = Field(attribute='sector__nombre', column_name='Sector')
    lote_nombre = Field(attribute='lote__nombre', column_name='Lote')
    huerto_nombre = Field(attribute='huerto__nombre', column_name='Huerto')
    asignado_nombre = Field(attribute='asignado__nombre', column_name='Asignado')

    class Meta:
        model = Procesos
        fields = ("trabajo", "fecha", "hora_asignada", "sector_nombre", "lote_nombre", "huerto_nombre", "estado", "asignado_nombre", "presupuesto", 'hora_creacion')
    
    def dehydrate(self, row):
        # Aquí puedes realizar alguna transformación adicional si es necesario
        return row
    

class JornadasResource(resources.ModelResource):
    asignado_nombre = Field(attribute='asignado__nombre', column_name='Asignado')
    sector_nombre = Field(attribute='sector__nombre', column_name='Sector')
    huerto_nombre = Field(attribute='huerto__nombre', column_name='Huerto')
    lote_nombre = Field(attribute='lote__nombre', column_name='Lote')
    
    

    class Meta:
        model = Jornada
        fields = ['asignado_nombre',  'fecha', 'nombre_tarea_1', 
                  'hora_inicio_tarea_1', 'hora_fin_tarea_1', 'cobro_tarea_1', 'nombre_tarea_2', 'hora_inicio_tarea_2', 
                  'hora_fin_tarea_2', 'cobro_tarea_2', 'nombre_tarea_3', 'hora_inicio_tarea_3', 'hora_fin_tarea_3', 'cobro_tarea_3','total_gasto_jornada','estado','detalle_gasto_total_tareas','detalle_gastos_total_extras'

                  'nombre_extra_1','gasto_extra_1','nombre_extra_2','gasto_extra_2','nombre_extra_3','gasto_extra_3','nombre_extra_1','gasto_extra_1','nombre_extra_2','gasto_extra_2','nombre_extra_3','gasto_extra_3',
                  'observacion']
    
    def dehydrate(self, row):
        # Aquí puedes realizar alguna transformación adicional si es necesario
        return row


class TrabajadorResource(resources.ModelResource):
    

    class Meta:
        model = Trabajador
        fields = ("nombre", "rut", "fecha_ingreso", "fecha_termino_contrato", "tipo_contraro", "cobro","trabajo_a_realizar",)
    
    def dehydrate(self, row):
        # Aquí puedes realizar alguna transformación adicional si es necesario
        return row
    


    