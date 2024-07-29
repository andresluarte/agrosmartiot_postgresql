from django.urls import path
from agrosmartiotweb import views

urlpatterns = [
    path('', views.home, name = "home"),


    


    
    path('gestiondetareas/', views.ProcesoList, name = "gestiondetareas"),
    path('api/', views.ProcesoListAPIView.as_view(),),
    path('exportar_proceso/', views.ExportToExcelViewProceso.as_view(), name='exportar_a_excel_proceso'),
    path('exportar_jornada/', views.ExportToExcelViewJornada.as_view(), name='exportar_a_excel_jornada'),
    path('exportar_trabajador/', views.ExportToExcelViewTrabajador.as_view(), name='exportar_a_excel_trabajador'),






    path('ayuda/', views.ayuda, name = "ayuda"),
 





    path('informes/', views.informes, name = "informes"),
    path('agregartarea/', views.agregartarea, name = "agregartarea"),
    
    #zona especifica
    path('gestion_zona/', views.gestion_zona, name = "gestion_zona"),
    path('agregarsector/', views.agregar_sector, name = "agregarsector"),
    path('agregar_huerto/<int:sector_id>/', views.agregar_huerto, name='agregar_huerto'),
    path('agregar_huerto_ss/', views.agregar_huerto_sin_sector, name='agregar_huerto_ss'),
    path('agregarlote/', views.agregar_lote, name = "agregarlote"),
    path('modificarsector/<id>', views.modificarsector, name = "modificarsector"),
    path('modificarhuerto/<id>', views.modificarhuerto, name = "modificarhuerto"),
    path('eliminarsector/<int:id>/', views.eliminarsector, name = "eliminarsector"),
    #eliminar huerto
    path('eliminarhuerto/<int:id>/', views.eliminarhuerto, name = "eliminarhuerto"),
    path('modificarlote/<id>', views.modificarlote, name = "modificarlote"),

      

    
    path('modificartarea/<id>', views.modificartarea, name = "modificartarea"),
    path('eliminartarea/<int:id>/', views.eliminartarea, name = "eliminartarea"),
    
    #url trabajadores
    path('gestiondetrabajadores/', views.TrabajadorList, name = "gestiondetrabajadores"),
    path('agregartrabajador/', views.agregartrabajador, name = "agregartrabajador"),
    path('modificartrabajadores/<id>', views.modificartrabajadores, name = "modificartrabajadores"),
    path('eliminartrabajador/<int:id>/', views.eliminartrabajador, name = "eliminartrabajador"),
    

    path('agregar_jornada/', views.agregar_jornada, name='agregar_jornada'),
    path('gestion_jornadas2/', views.JornadaListView.as_view(), name = "gestion_jornadas2"),
    path('gestion_jornadas/', views.JornadaList, name='gestion_jornadas'),
    
    
    path('modificarjornada/<id>', views.modificarjornada, name = "modificarjornada"),
    path('eliminarjornada/<int:id>/', views.eliminarjornada, name = "eliminarjornada"),

    path('cargar_huertos/', views.cargar_huertos, name='cargar_huertos'),
    path('cargar_lotes/', views.cargar_lotes, name='cargar_lotes'),
  #sensor
    path('receive-data/', views.receive_data, name='receive_data'),

    path('obtener_cobro/', views.obtener_cobro_view, name='obtener_cobro'),


    path('api/temperature-humidity/', views.  TemperatureHumidityAPIView.as_view(), name='temperature-humidity'),
    path('tiemporeal/', views.combined_data_view, name='tiemporeal'),



    #registration
    path('obtener_cobro/', views.obtener_cobro_view, name='obtener_cobro'),

    #registration
    path('register/', views.register, name='register'),
    path('my_login/', views.my_login, name='my_login'),
    path('user_logout/', views.user_logout, name='user_logout'),
   


    path('gestion_finanzas/', views.FinanzasList, name='gestion_finanzas'),
   
    path('agregar_gasto_financiero/', views.agregar_gasto_financiero, name='agregar_gasto_financiero'),

    path('receive-data-soil/', views.receive_data_soil, name='receive_data_soil'),
    path('tiemporealsoil/', views.combined_data_view_soil, name='combined_data_view_soil'),


  


]

