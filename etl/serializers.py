from rest_framework import serializers
from .models import ETLLog


class ETLLogSerializer(serializers.ModelSerializer):

    usuario = serializers.StringRelatedField()

    class Meta:
        model = ETLLog
        fields = [
            'id',
            'usuario',
            'fecha_inicio',
            'fecha_fin',
            'tiempo_ejecucion',
            'registros_extraidos',
            'registros_duplicados',
            'registros_nulos',
            'registros_fuera_rango',
            'registros_cargados',
            'estado',
            'mensaje',
            'archivo_fuente',
        ]