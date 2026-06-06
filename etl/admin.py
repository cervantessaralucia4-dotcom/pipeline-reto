from django.contrib import admin
from .models import ETLLog

@admin.register(ETLLog)
class ETLLogAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'usuario', 'fecha_inicio', 'estado',
        'registros_extraidos', 'registros_cargados', 'tiempo_ejecucion'
    ]
    list_filter  = ['estado', 'fecha_inicio']
    readonly_fields = [
        'fecha_inicio', 'fecha_fin', 'tiempo_ejecucion',
        'registros_extraidos', 'registros_duplicados',
        'registros_nulos', 'registros_fuera_rango', 'registros_cargados',
    ]