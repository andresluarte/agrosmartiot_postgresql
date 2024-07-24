from typing import Any, Dict
from django.shortcuts import render, redirect, get_object_or_404
from .models import Procesos ,Trabajador,Jornada,Sector,Huerto,Lote,Finanzas,FinanzasPorMes,GastoFinanciero
from .forms import ContactoForm,ProcesoForm,ProcesoModificarForm,TrabajadorForm,FormatoForm,TrabajadorModificarForm,JornadaModificarForm,SectorModificarForm,HuertoModificarForm,LoteModificarForm,GastoFinancieroForm
from django.contrib import messages
from django.http import Http404
#api
from .serializers import ProcesoSerializer
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test



#llamada de filtros

from .forms import FiltroEstado
from .filters import ProcesoFilter,TrabajadorFilter,JornadaFilter

#List view

from django.views.generic.list import ListView
from django.views import View
#paginador 

from django.core.paginator import Paginator

#resource exportar excel
from .admin import ProcesosResource,JornadasResource,TrabajadorResource


def home (request):
    return render (request, 'agrosmart/home.html')

def informes(request):

    return render(request, 'agrosmart/informes.html')

# def gestiondetareas(request):
#     proceso_filter = ProcesoFilter(request.GET,queryset=Procesos.objects.all())
#     data = {
#         'form':proceso_filter.form,
#         'procesos' : proceso_filter.qs

#     }

#     return render(request, 'agrosmart/gestiondetareas.html',data)

class ProcesoListView(ListView):
    queryset = Procesos.objects.all()
    form_class = FormatoForm
    template_name = 'agrosmart/gestiondetareas.html'
    context_object_name = 'procesos'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ProcesoFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.filterset.form
        return context
#exportar tarea (proceso)       
class ExportToExcelViewProceso(View):
    def get(self, request):
        queryset = ProcesoFilter(request.GET, queryset=Procesos.objects.all()).qs
        dataset = ProcesosResource().export(queryset=queryset)
        response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="procesos.xls"'
        return response

    def post(self, request):
        queryset = ProcesoFilter(request.POST, queryset=Procesos.objects.all()).qs
        dataset = ProcesosResource().export(queryset=queryset)
        response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="procesos.xls"'
        return response
    
#exportar excel jornada
class ExportToExcelViewJornada(View):
    def get(self, request):
        queryset = JornadaFilter(request.GET, queryset=Jornada.objects.all()).qs
        dataset = JornadasResource().export(queryset=queryset)
        response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Jornada.xls"'
        return response

    def post(self, request):
        queryset = JornadaFilter(request.POST, queryset=Jornada.objects.all()).qs
        dataset = JornadasResource().export(queryset=queryset)
        response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Jornada.xls"'
        return response

class ExportToExcelViewTrabajador(View):
    def get(self, request):
        queryset = TrabajadorFilter(request.GET, queryset=Trabajador.objects.all()).qs
        dataset = TrabajadorResource().export(queryset=queryset)
        response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="trabajador.xls"'
        return response

    def post(self, request):
        queryset = TrabajadorFilter(request.POST, queryset=Jornada.objects.all()).qs
        dataset = TrabajadorResource().export(queryset=queryset)
        response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Jornada.xls"'
        return response

    
class ProcesoListAPIView(ListAPIView):
    queryset = Procesos.objects.all()
    serializer_class = ProcesoSerializer



        
    




def ayuda(request):

    contacto = {
        'form' : ContactoForm()
    }

    return render(request, 'agrosmart/ayuda.html',contacto)

def tiemporeal(request):

    return render(request, 'agrosmart/tiemporeal.html')


def agregartarea(request):

    data = {
        'form' : ProcesoForm()
    }

    if request.method =='POST':
        formulario = ProcesoForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request,"Tarea Registrada")
        else:
            data["form"] = formulario

        

    return render(request, 'agrosmart/agregartarea.html',data)

def modificartarea(request,id):
    proceso = get_object_or_404(Procesos,id=id)
    data ={
        'form' : ProcesoModificarForm(instance=proceso)
    }

    if request.method == 'POST':
        formulario = ProcesoModificarForm(data=request.POST,instance=proceso,files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request,"Modificado Correctamente")
            
        data["form"] = formulario

    return render(request, 'agrosmart/modificartarea.html',data)

def modificartrabajadores(request,id):
    trabajadores = get_object_or_404(Trabajador,id=id)
    data ={
        'form' : TrabajadorModificarForm(instance=trabajadores)
    }

    if request.method == 'POST':
        formulario = TrabajadorModificarForm(data=request.POST,instance=trabajadores,files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request,"Modificado Correctamente")
            
        data["form"] = formulario

    return render(request, 'agrosmart/trabajadores/modificartrabajadores.html',data)

def eliminartarea(request, id):
    proceso = get_object_or_404(Procesos, id=id)
    proceso.delete()
    messages.success(request, "Eliminado Correctamente")
    return redirect('gestiondetareas')



#AGREGAR ZONA ESPECIFICA

#AGREGAR filtros
#AGREGAR TRABAJADOR 

def agregartrabajador(request):

    data = {
        'form' : TrabajadorForm()
    }

    if request.method =='POST':
        formulario = TrabajadorForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request,"Trabajador Registrado")
        else:
            data["form"] = formulario
    return render(request, 'agrosmart/trabajadores/agregartrabajador.html',data)

class TrabajadorListView(ListView):
    queryset = Trabajador.objects.all()



    template_name = 'agrosmart/trabajadores/gestiondetrabajadores.html'
    context_object_name = 'trabajador'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset=TrabajadorFilter(self.request.GET,queryset=queryset)
        return self.filterset.qs
    def get_context_data(self, **kwargs):

        context= super().get_context_data(**kwargs)
        context['form']=self.filterset.form
        return context
    
def modificarjornada(request,id):
    trabajadores = get_object_or_404(Jornada,id=id)
    data ={
        'form' : JornadaModificarForm(instance=trabajadores)
    }

    if request.method == 'POST':
        formulario = JornadaModificarForm(data=request.POST,instance=trabajadores,files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request,"Jornada Modificada Correctamente")
            
        data["form"] = formulario

    return render(request, 'agrosmart/jornada/modificarjornada.html',data)

def eliminarjornada(request, id):
    jornada = get_object_or_404(Jornada, id=id)
    jornada.delete()
    messages.success(request, "Jornada Eliminada Correctamente")
    return redirect('gestion_jornadas')

#exportar excel
def eliminartrabajador(request, id):
    proceso = get_object_or_404(Trabajador, id=id)
    proceso.delete()
    messages.success(request, "Trabajador Eliminado Correctamente")
    return redirect('TrabajadorList')

##sensor



from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt




#jornada

from django.shortcuts import render, redirect
from .forms import JornadaForm

def agregar_jornada(request):
    if request.method == 'POST':
        form = JornadaForm(request.POST)
        if form.is_valid():
            form = form.save()
            return redirect('gestion_jornadas')
    else:
        form = JornadaForm()
    
    return render(request, 'agrosmart/jornada/crear_jornada.html', {'form': form})

class JornadaListView(ListView):
    queryset = Jornada.objects.all()
    form_class = FormatoForm
    paginate_by = 4
    template_name = 'agrosmart/jornada/gestion_jornadas.html'
    context_object_name = 'jornadas'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = JornadaFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.filterset.form
        return context

@login_required(login_url="my_login")
def JornadaList(request):
    context = { }
   
    filtered_jornadas = JornadaFilter(
        request.GET,
        queryset=Jornada.objects.all()

    )
    
    context['filtered_jornadas'] = filtered_jornadas
    paginated_filtered_jornadas = Paginator(filtered_jornadas.qs,3)
    page_number = request.GET.get('page')
    jornada_page_obj = paginated_filtered_jornadas.get_page(page_number)

    context['jornada_page_obj'] = jornada_page_obj
    


    return render(request, 'agrosmart/jornada/gestion_jornadas.html', context=context)

@login_required(login_url="my_login")
def TrabajadorList(request):
    context ={}

    filtered_trabajador = TrabajadorFilter(
        request.GET,
        queryset=Trabajador.objects.all()

    )
    context ['filtered_trabajador'] = filtered_trabajador
    paginated_filtered_trabajador = Paginator(filtered_trabajador.qs,8)
    page_number = request.GET.get('page')
    trabajador_page_obj = paginated_filtered_trabajador.get_page(page_number)

    context['trabajador_page_obj']= trabajador_page_obj 
    return render(request, 'agrosmart/trabajadores/gestiondetrabajadores.html', context=context)
 
def ProcesoList(request):
    context = { }
   
    filtered_proceso = ProcesoFilter(
        request.GET,
        queryset=Procesos.objects.all()

    )
    
    context['filtered_proceso'] = filtered_proceso
    paginated_filtered_proceso = Paginator(filtered_proceso.qs,8)
    page_number = request.GET.get('page')
    proceso_page_obj = paginated_filtered_proceso.get_page(page_number)

    context['proceso_page_obj'] = proceso_page_obj
    


    return render(request, 'agrosmart/gestiondetareas.html', context=context)

def gestion_zona(request):
    sectores = Sector.objects.all()

    context = {
        'sectores': sectores
    }

    return render(request, "agrosmart/zona/gestion_zona.html", context)




from django.shortcuts import render, redirect
from .forms import SectorForm, HuertoForm, LoteForm

def agregar_sector(request):
    if request.method == "POST":
        form = SectorForm(request.POST)
        if form.is_valid():
            sector = form.save()  # Obtén el sector recién creado
            # Redirige al formulario de creación de Huerto y pasa el sector como contexto
            return redirect('agregarhuerto', sector_id=sector.id)
    else:
        form = SectorForm()
    return render(request, 'agrosmart/zona/agregarsector.html', {'form': form})

def modificarsector(request,id):
    sectores = get_object_or_404(Sector,id=id)
    data ={
        'form' : SectorModificarForm(instance=sectores)
    }

    if request.method == 'POST':
        formulario = SectorModificarForm(data=request.POST,instance=sectores,files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request,"Modificado Correctamente")
            
        data["form"] = formulario

    return render(request, 'agrosmart/zona/modificarsector.html',data)

def modificarhuerto(request,id):
    huertos = get_object_or_404(Huerto,id=id)
    data = {
        'form':HuertoModificarForm(instance=huertos)
       
    }
    if request.method == 'POST':
        formulario = HuertoModificarForm(data=request.POST,instance=huertos,files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request,"Huerto Modificado Correctamente")

        data["form"] = formulario
        return redirect("gestion_zona")

    return render(request, 'agrosmart/zona/modificarhuerto.html',data)

def modificarlote(request,id):
    lotes = get_object_or_404(Lote,id=id)
    data = {
        'form':LoteModificarForm(instance=lotes)
       
    }
    if request.method == 'POST':
        formulario = LoteModificarForm(data=request.POST,instance=lotes,files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request,"Lote Modificado Correctamente")

        data["form"] = formulario
        return redirect("gestion_zona")

    return render(request, 'agrosmart/zona/modificarlote.html',data)


def agregar_sector(request):
    if request.method == "POST":
        form = SectorForm(request.POST)
        if form.is_valid():
            sector = form.save()  # Obtén el sector recién creado
            # Redirige al formulario de creación de Huerto y pasa el sector como contexto
            return redirect('agregar_huerto', sector_id=sector.id)
    else:
        form = SectorForm()
    return render(request, 'agrosmart/zona/agregarsector.html', {'form': form})

def agregar_huerto_sin_sector(request):
    if request.method == 'POST':
        form = HuertoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('agregarlote')
    else:
        form = HuertoForm()
    return render(request, 'agrosmart/zona/agregarhuerto.html', {'form': form})

def agregar_huerto(request, sector_id):
    sector = Sector.objects.get(id=sector_id)  # Obtiene el sector del contexto
    if request.method == "POST":
        form = HuertoForm(request.POST)
        if form.is_valid():
            huerto = form.save(commit=False)
            huerto.sector = sector  # Asigna el sector al huerto
            huerto.save()
            # Realiza las acciones necesarias y redirige a donde desees
    else:
        form = HuertoForm(initial={'sector': sector})  # Establece el sector como valor predeterminado
    return render(request, 'agrosmart/zona/agregarhuerto.html', {'form': form})

def agregar_lote(request):
    if request.method == 'POST':
        form = LoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('agregarlote')
    else:
        form = LoteForm()
    return render(request, 'agrosmart/zona/agregarlote.html', {'form': form})

def cargar_huertos(request):
    sector_id = request.GET.get('sector_id')
    huertos = Huerto.objects.filter(sector_id=sector_id)
    huertos_list = list(huertos.values('id', 'nombre'))
    return JsonResponse({'huertos': huertos_list})

def cargar_lotes(request):
    huerto_id = request.GET.get('huerto_id')
    if huerto_id == 'todos':
        # Si es 'todos', podrías devolver todos los lotes de ese sector si lo deseas
        # Aquí solo como ejemplo, retornamos todos los lotes
        lotes = Lote.objects.all()
    else:
        lotes = Lote.objects.filter(huerto_id=huerto_id)
    lotes_list = list(lotes.values('id', 'nombre'))
    return JsonResponse({'lotes': lotes_list})



def eliminarsector(request, id):
    sector = get_object_or_404(Sector, id=id)
    sector.delete()
    messages.success(request, "Sector Eliminado Correctamente")
    return redirect('gestion_zona')

def eliminarhuerto(request, id):
    huerto = get_object_or_404(Huerto, id=id)
    huerto.delete()
    messages.success(request, "Sector Eliminado Correctamente")
    return redirect ('gestion_zona')
    


# def eliminartarea(request, id):
#     proceso = get_object_or_404(Procesos, id=id)
#     proceso.delete()
#     messages.success(request, "Eliminado Correctamente")
#     return redirect('gestiondetareas')
# en views.py
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def receive_data(request):
    if request.method == 'POST':
        # Procesar los datos aquí
        data = request.POST
        temperature = data.get('temperature')
        humidity = data.get('humidity')
        ds18b20_temp = data.get('ds18b20_temp')

        # Lógica para manejar los datos
        return JsonResponse({"status": "success"})
    else:
        return JsonResponse({"message": "Invalid request method"}, status=405)
from django.http import JsonResponse

def obtener_cobro_view(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        trabajador_id = request.GET.get('trabajador_id')
        try:
            trabajador = Trabajador.objects.get(id=trabajador_id)
            cobro = trabajador.cobro
            data = {'cobro': cobro}
            return JsonResponse(data)
        except Trabajador.DoesNotExist:
            return JsonResponse({'error': 'Trabajador no encontrado'})
    else:
        return JsonResponse({'error': 'No es una solicitud AJAX'})
    
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import TemperatureHumidity
from .serializers import TemperatureHumiditySerializer

class TemperatureHumidityAPIView(APIView):
    def post(self, request, format=None):
        serializer = TemperatureHumiditySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
def temperature_humidity_list(request):
    data = TemperatureHumidity.objects.all()
    return render(request, 'agrosmart/tiemporeal.html', {'data': data})

#authentication 
from django.contrib.auth.models import Group

from django.contrib.auth.forms import AuthenticationForm    
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate,login,logout

from . forms import CreateUserForm,LoginForm
from django.contrib.auth.decorators import login_required

def register(request):
    form =CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("my_login")
    context = {'registerform':form}

    return render (request,'agrosmart/registration/register.html',context=context )

def my_login(request):
    form = LoginForm()  # Inicializa la variable form aquí
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect("home")
    context = {"form": form}
    return render(request, 'agrosmart/registration/my-login.html', context=context)


def user_logout(request):
    auth.logout(request)
    return redirect ("home")

def FinanzasList(request):
    finanzas = Finanzas.objects.all()
    finanzas_por_mes = FinanzasPorMes.objects.all()
    gastos_por_mes = GastoFinanciero.objects.gastos_por_mes()
    
    return render(request, 'agrosmart/finanzas/gestion_finanzas.html', {'finanzas': finanzas,'finanzas_por_mes': finanzas_por_mes,'gastos_por_mes':gastos_por_mes})

###gasto financiero 
def agregar_gasto_financiero(request):
    if request.method == 'POST':
        form = GastoFinancieroForm(request.POST)
        if form.is_valid():
            form.save()  # El método save() en el modelo ya maneja la actualización de FinanzasPorMes
            return redirect('gestion_finanzas')  # Reemplaza con el nombre de la vista a la que quieres redirigir después de guardar
    else:
        form = GastoFinancieroForm()
    
    return render(request, 'agrosmart/finanzas/agregar_gasto_financiero.html', {'form': form})

