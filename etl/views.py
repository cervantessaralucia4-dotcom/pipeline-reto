# ═══════════════════════════════════════════════════════════════
#  etl/views.py
#  Endpoints:
#    POST /api/etl/run/         — ejecuta el ETL
#    GET  /api/etl/historial/   — lista todos los logs
#    GET  /api/etl/historial/<id>/ — detalle de un log
# ═══════════════════════════════════════════════════════════════
import os
from datetime import datetime, timezone

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from patients.models import Patient
from .models import ETLLog
from .serializers import ETLLogSerializer
from .etl_process import run_etl


# ── POST /api/etl/run/ ────────────────────────────────────────
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def run_etl_view(request):
    """
    Ejecuta el pipeline ETL completo.
    Acepta opcionalmente el campo 'archivo' en el body
    para usar un path distinto al default.
    """
    archivo = request.data.get(
        'archivo',
        'datasets/dataset_clinico_etl_1800_registros.xlsx'
    )

    # Crear log inicial
    log = ETLLog.objects.create(
        usuario=request.user,
        estado='en_proceso',
        archivo_fuente=archivo,
    )

    try:
        stats = run_etl(file_path=archivo)

        # Cargar pacientes limpios en la BD
        df = stats.get('df_limpio')
        if df is not None:
            Patient.objects.all().delete()     # limpia antes de reinsertar
            pacientes = []
            for _, row in df.iterrows():
                try:
                    pacientes.append(Patient(
                        first_name=str(row['nombres']).strip(),
                        last_name=str(row['apellidos']).strip(),
                        age=int(row['edad']),
                        sex='M' if str(row['sexo']).upper() == 'M' else 'F',
                        weight=float(row['peso']),
                        height=float(row['altura']),
                        systolic_pressure=int(row['presión_sistólica']),
                        diastolic_pressure=int(row['presión_diastólica']),
                        heart_rate=int(row['frecuencia_cardiaca']),
                        glucose=float(row['glucosa']),
                        cholesterol=float(row['colesterol']),
                        oxygen_saturation=float(row['saturación_oxígeno']),
                        temperature=float(row['temperatura']),
                        family_history=bool(row['antecedentes_familiares']),
                        smoker=bool(row['fumador']),
                        alcohol_consumption=bool(row['consumo_alcohol']),
                        physical_activity=str(row['actividad_física']),
                        preliminary_diagnosis=str(row['diagnóstico_preliminar']),
                        disease_risk=str(row['riesgo_calculado']),
                        consultation_date=str(row['fecha_consulta'])[:10],
                    ))
                except Exception:
                    continue

            Patient.objects.bulk_create(pacientes, ignore_conflicts=True)

        # Actualizar log con resultados
        log.fecha_fin             = datetime.now(timezone.utc)
        log.tiempo_ejecucion      = stats['tiempo_ejecucion']
        log.registros_extraidos   = stats['registros_extraidos']
        log.registros_duplicados  = stats['registros_duplicados']
        log.registros_nulos       = stats['registros_nulos']
        log.registros_fuera_rango = stats['registros_fuera_rango']
        log.registros_cargados    = stats['registros_cargados']
        log.estado                = 'exitoso'
        log.mensaje               = stats['mensaje']
        log.save()

        return Response({
            'estado':               'exitoso',
            'log_id':               log.pk,
            'registros_extraidos':  log.registros_extraidos,
            'registros_duplicados': log.registros_duplicados,
            'registros_nulos':      log.registros_nulos,
            'registros_fuera_rango': log.registros_fuera_rango,
            'registros_cargados':   log.registros_cargados,
            'tiempo_ejecucion':     log.tiempo_ejecucion,
            'mensaje':              log.mensaje,
        }, status=status.HTTP_200_OK)

    except Exception as e:
        log.estado  = 'fallido'
        log.mensaje = str(e)
        log.fecha_fin = datetime.now(timezone.utc)
        log.save()

        return Response({
            'estado':  'fallido',
            'log_id':  log.pk,
            'mensaje': str(e),
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ── GET /api/etl/historial/ ───────────────────────────────────
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def etl_historial(request):
    """Lista el historial de ejecuciones ETL."""
    logs = ETLLog.objects.all()[:50]
    serializer = ETLLogSerializer(logs, many=True)
    return Response(serializer.data)


# ── GET /api/etl/historial/<id>/ ──────────────────────────────
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def etl_detalle(request, pk):
    """Detalle de un log ETL específico."""
    try:
        log = ETLLog.objects.get(pk=pk)
    except ETLLog.DoesNotExist:
        return Response({'error': 'Log no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ETLLogSerializer(log)
    return Response(serializer.data)