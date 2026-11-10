"""Conatacoch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Administrador import views


urlpatterns = [

    # Página principal
    path('', views.pagina_principal, name='paginaPrincipal'),


    #--------- CONDUCTORES -------------------

    path('conductores/', views.todos_conductores, name='conductores'),

    path('conductorADD/', views.crear_conductor, name='crearConductor'),

    path('conductorEdit/<str:conductor_rut>/',
         views.cargar_editar_conductor, name='editarConductor'),

    path('conductorEditado/<str:conductor_rut>/',
         views.editar_conductor, name='conductorEditado'),

    path('conductorDel/<str:conductor_rut>/',
         views.eliminar_conductor, name='eliminarConductor'),


    #--------- AUTOMOVILES -------------------

    path('automoviles/',
         views.todos_automoviles, name='automoviles'),

    path('automovilADD/',
         views.crear_automovil, name='crearAutomovil'),

    path('automovilEdit/<int:automovil_id>/',
         views.cargar_editar_automovil, name='editarAutomovil'),

    path('automovilEditado/<int:automovil_id>/',
         views.editar_automovil, name='automovilEditado'),

    path('automovilDel/<int:automovil_id>/',
         views.eliminar_automovil, name='eliminarAutomovil'),


    #--------- ADMINISTRACION Y AUTENTICACION -------------------

    path('admin/', admin.site.urls),

    path('accounts/', include('django.contrib.auth.urls')),
]
