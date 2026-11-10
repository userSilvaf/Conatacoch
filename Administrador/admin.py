from django.contrib import admin
from Administrador.models import Conductor, Automovil

# Register your models here.
#--------- ADMINISTRACION CONDUCTORES -------------------

class ConductorAdmin(admin.ModelAdmin):

    list_display = [
        'rut',
        'nombre_completo',
        'fono_celular',
        'tipo_licencia',
        'fecha_vencimiento'
    ]


#--------- ADMINISTRACION AUTOMOVILES -------------------

class AutomovilAdmin(admin.ModelAdmin):

    list_display = [
        'patente',
        'marca',
        'modelo',
        'anio',
        'combustible',
        'permiso_vencimiento',
        'revision_vencimiento',
        'seguro_vencimiento'
    ]

    search_fields = [
        'patente',
        'marca',
        'modelo'
    ]

    list_filter = [
        'marca',
        'combustible'
    ]

    ordering = ['patente']

    fieldsets = (

        ('Datos del automóvil', {
            'fields': (
                'marca',
                'modelo',
                'anio',
                'combustible',
                'patente'
            )
        }),

        ('Permiso de circulación', {
            'fields': (
                'permiso_comuna',
                'permiso_fecha_otorgacion',
                'permiso_vencimiento'
            )
        }),

        ('Revisión técnica', {
            'fields': (
                'revision_planta',
                'revision_comuna',
                'revision_vencimiento'
            )
        }),

        ('Seguro obligatorio', {
            'fields': (
                'seguro_compania',
                'seguro_prima',
                'seguro_vencimiento'
            )
        }),
    )


#--------- REGISTRO DE MODELOS -------------------

admin.site.register(Conductor, ConductorAdmin)
admin.site.register(Automovil, AutomovilAdmin)

