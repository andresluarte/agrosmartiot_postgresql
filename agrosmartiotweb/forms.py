from django import forms 
from .models import Procesos,Contacto,Trabajador,Sector,Huerto,Lote,GastoFinanciero

class DateInput(forms.DateInput):
    input_type='date'

class TimePickerInput(forms.TimeInput):
    input_type = 'time'

class ProcesoForm(forms.ModelForm):
    
    class Meta:
        model = Procesos
        fields =  ["trabajo","fecha","hora_asignada","sector","huerto","lote","asignado","presupuesto","observacion"]

        widgets={
            "fecha":DateInput,
            
        }
    

class ContactoForm(forms.ModelForm):

    class Meta:
        model = Contacto
        fields = '__all__'

class ProcesoModificarForm(forms.ModelForm):
    
    class Meta:
        model = Procesos
        fields =  ["trabajo","fecha","hora_asignada","sector","huerto","lote","estado","asignado","presupuesto","observacion"]

        widgets={
            "fecha":forms.SelectDateWidget,
            
        }
class TrabajadorModificarForm(forms.ModelForm):
    
    class Meta:
        model = Trabajador
        fields =  ["nombre","cobro","trabajo_a_realizar"]
        
            
        



        
class FiltroEstado(forms.Form):
    estado = forms.CharField()

class TrabajadorForm(forms.ModelForm):

    class Meta:
        model = Trabajador
        fields = ['nombre','rut','tipo_contraro','fecha_ingreso', 'fecha_termino_contrato','cobro','trabajo_a_realizar']
        widgets={
            "fecha_ingreso":DateInput(),
            "fecha_termino_contrato": DateInput(),
   
        }
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
        # Establece un valor predeterminado para el campo fecha_termino_contrato
            self.fields['fecha_termino_contrato'].initial = 'Sin Fecha Termino'



####formato

FORMAT_CHOICES = (
    ('xls','xls'),
    ('csv','csv')
)

class FormatoForm(forms.Form):
    format = forms.ChoiceField(choices=FORMAT_CHOICES,widget=forms.Select(attrs={'class':'form-select'}))

from .models import Jornada
#jornada


HORAS_PERMITIDAS = [
    '06:00', '06:30', '07:00', '07:30', '08:00', '08:30', '09:00', '09:30', '10:00',
    '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30', '14:00', '14:30',
    '15:00', '15:30', '16:00', '16:30', '17:00', '17:30', '18:00', '18:30', '19:00',
    '19:30', '20:00', '20:30', '21:00', '21:30', '22:00', '22:30', '23:00',
]

class CustomTimePickerInput(DateInput):
    def __init__(self, attrs=None, format=None):
        super().__init__(attrs={'type': 'time', 'step': '1800', 'list': 'horas-permitidas'})
    
    def render(self, name, value, attrs=None, renderer=None):
        rendered = super().render(name, value, attrs, renderer)
        rendered += '<datalist id="horas-permitidas">'
        for hora in HORAS_PERMITIDAS:
            rendered += f'<option value="{hora}">'
        rendered += '</datalist>'
        return rendered


class JornadaForm(forms.ModelForm):
    
    class Meta:
        model = Jornada
        fields = ['asignado',  'sector', 'huerto', 'lote', 'fecha', 'nombre_tarea_1', 
                  'hora_inicio_tarea_1', 'hora_fin_tarea_1', 'cobro_tarea_1', 'nombre_tarea_2', 'hora_inicio_tarea_2', 
                  'hora_fin_tarea_2', 'cobro_tarea_2', 'nombre_tarea_3', 'hora_inicio_tarea_3', 'hora_fin_tarea_3', 'cobro_tarea_3',

                  'nombre_extra_1','gasto_extra_1','nombre_extra_2','gasto_extra_2','nombre_extra_3','gasto_extra_3','nombre_extra_1','gasto_extra_1','nombre_extra_2','gasto_extra_2','nombre_extra_3','gasto_extra_3',
                  'observacion']
        widgets = {
            "fecha": DateInput(),
            "hora_inicio_tarea_1": CustomTimePickerInput(),
            "hora_fin_tarea_1": CustomTimePickerInput(),
            "hora_inicio_tarea_2": CustomTimePickerInput(),
            "hora_fin_tarea_2": CustomTimePickerInput(),
            "hora_inicio_tarea_3": CustomTimePickerInput(),
            "hora_fin_tarea_3": CustomTimePickerInput(),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        cobro_por_hora = instance.asignado.cobro if instance.asignado else None

        

        def calcular_cobro_tarea(hora_inicio, hora_fin):
            if hora_inicio and hora_fin and cobro_por_hora:
                hora_inicio = hora_inicio.hour + hora_inicio.minute / 60
                hora_fin = hora_fin.hour + hora_fin.minute / 60
                horas_trabajadas = hora_fin - hora_inicio
                return round(horas_trabajadas * cobro_por_hora, 2)
            return None

        # Calcular los cobros de las tareas
        instance.cobro_tarea_1 = calcular_cobro_tarea(self.cleaned_data.get('hora_inicio_tarea_1'), self.cleaned_data.get('hora_fin_tarea_1'))
        instance.cobro_tarea_2 = calcular_cobro_tarea(self.cleaned_data.get('hora_inicio_tarea_2'), self.cleaned_data.get('hora_fin_tarea_2'))
        instance.cobro_tarea_3 = calcular_cobro_tarea(self.cleaned_data.get('hora_inicio_tarea_3'), self.cleaned_data.get('hora_fin_tarea_3'))

        # Sumar los cobros de las tareas para calcular detalle_gasto_total_tareas
        cobros_tareas = [instance.cobro_tarea_1, instance.cobro_tarea_2, instance.cobro_tarea_3]
        instance.detalle_gasto_total_tareas = sum(filter(None, cobros_tareas))

    # Calcular detalle_gastos_total_extras
        gastos_extras = [instance.gasto_extra_1, instance.gasto_extra_2, instance.gasto_extra_3]
        instance.detalle_gastos_total_extras = sum(filter(None, gastos_extras))

        # Calcular total_gasto_jornada
        instance.total_gasto_jornada = instance.detalle_gasto_total_tareas + instance.detalle_gastos_total_extras

        if commit:
            instance.save()
        return instance

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['cobro_tarea_1', 'cobro_tarea_2', 'cobro_tarea_3']:
            self.fields[field_name].widget.attrs['readonly'] = False


    

class JornadaModificarForm(forms.ModelForm):
    
    class Meta:
        model = Jornada
        fields = ['asignado',  'sector', 'huerto', 'lote', 'fecha', 'estado','nombre_tarea_1', 
                  'hora_inicio_tarea_1', 'hora_fin_tarea_1', 'cobro_tarea_1', 'nombre_tarea_2', 'hora_inicio_tarea_2', 
                  'hora_fin_tarea_2', 'cobro_tarea_2', 'nombre_tarea_3', 'hora_inicio_tarea_3', 'hora_fin_tarea_3', 'cobro_tarea_3',

                  'nombre_extra_1','gasto_extra_1','nombre_extra_2','gasto_extra_2','nombre_extra_3','gasto_extra_3','nombre_extra_1','gasto_extra_1','nombre_extra_2','gasto_extra_2','nombre_extra_3','gasto_extra_3',
                  'observacion']

        
    def save(self, commit=True):
        instance = super().save(commit=False)
        cobro_por_hora = instance.asignado.cobro if instance.asignado else None

        

        def calcular_cobro_tarea(hora_inicio, hora_fin):
            if hora_inicio and hora_fin and cobro_por_hora:
                hora_inicio = hora_inicio.hour + hora_inicio.minute / 60
                hora_fin = hora_fin.hour + hora_fin.minute / 60
                horas_trabajadas = hora_fin - hora_inicio
                return round(horas_trabajadas * cobro_por_hora, 2)
            return None

        # Calcular los cobros de las tareas
        instance.cobro_tarea_1 = calcular_cobro_tarea(self.cleaned_data.get('hora_inicio_tarea_1'), self.cleaned_data.get('hora_fin_tarea_1'))
        instance.cobro_tarea_2 = calcular_cobro_tarea(self.cleaned_data.get('hora_inicio_tarea_2'), self.cleaned_data.get('hora_fin_tarea_2'))
        instance.cobro_tarea_3 = calcular_cobro_tarea(self.cleaned_data.get('hora_inicio_tarea_3'), self.cleaned_data.get('hora_fin_tarea_3'))

        # Sumar los cobros de las tareas para calcular detalle_gasto_total_tareas
        cobros_tareas = [instance.cobro_tarea_1, instance.cobro_tarea_2, instance.cobro_tarea_3]
        instance.detalle_gasto_total_tareas = sum(filter(None, cobros_tareas))

    # Calcular detalle_gastos_total_extras
        gastos_extras = [instance.gasto_extra_1, instance.gasto_extra_2, instance.gasto_extra_3]
        instance.detalle_gastos_total_extras = sum(filter(None, gastos_extras))

        # Calcular total_gasto_jornada
        instance.total_gasto_jornada = instance.detalle_gasto_total_tareas + instance.detalle_gastos_total_extras

        if commit:
            instance.save()
        return instance

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['cobro_tarea_1', 'cobro_tarea_2', 'cobro_tarea_3']:
            self.fields[field_name].widget.attrs['readonly'] = False



from django import forms
from .models import Sector, Huerto, Lote

class SectorForm(forms.ModelForm):
    class Meta:
        model = Sector
        fields = ['nombre','latitud','longitud']

class HuertoForm(forms.ModelForm):
    class Meta:
        model = Huerto
        fields = ['nombre', 'sector']

class LoteForm(forms.ModelForm):
    class Meta:
        model = Lote
        fields = ['nombre', 'huerto']

class SectorForm(forms.ModelForm):
    google_maps_link = forms.URLField(
        max_length=200, 
        required=False,
        label="Enlace de Google Maps (opcional)"
    )

    class Meta:
        model = Sector
        fields = ['nombre', 'latitud', 'longitud', 'google_maps_link']

    def clean(self):
        cleaned_data = super().clean()
        lat = cleaned_data.get("latitud")
        lng = cleaned_data.get("longitud")
        link = cleaned_data.get("google_maps_link")

        if not link and (not lat or not lng):
            raise forms.ValidationError("Debes proporcionar coordenadas o un enlace de Google Maps.")
        
class HuertoModificarForm(forms.ModelForm):
    class Meta:
        model = Huerto
        fields = ['nombre', 'sector']
class LoteModificarForm(forms.ModelForm):
    class Meta:
        model = Lote
        fields = ['nombre', 'huerto']
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User

from django import forms

from django.forms.widgets import PasswordInput,TextInput


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())

    
class GastoFinancieroForm(forms.ModelForm):
    class Meta:
        model = GastoFinanciero
        fields = ['nombre_gasto', 'monto', 'fecha_correspondiente', 'observacion']
        widgets = {
            'fecha_correspondiente': forms.DateInput(attrs={'type': 'date'}),
        }



