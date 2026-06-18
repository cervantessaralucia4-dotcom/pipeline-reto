from datetime import datetime, timezone
import pandas as pd
import numpy as np
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from authentication.permissions import IsAdministrador, IsAnalista, IsMedicoOrAnalista
from patients.models import Patient
from .models import ETLLog
from .serializers import ETLLogSerializer
from .etl_process import run_etl


@extend_schema(
    tags=['ETL'],
    summary='Ejecutar pipeline ETL completo',
    description=(
        'Ejecuta el pipeline ETL sobre el dataset clínico original. '
        'Extrae el Excel, elimina duplicados, trata nulos, valida rangos, '
        'normaliza variables y carga pacientes limpios en BD. '
        'Acceso: Analista y Administrador.'
    ),
)
@api_view(['POST'])
@permission_classes([IsAnalista])
def run_etl_view(request):
    archivo = request.data.get('archivo', 'datasets/dataset_clinico_etl_1800_registros.xlsx')
    log = ETLLog.objects.create(usuario=request.user, estado='en_proceso', archivo_fuente=archivo)

    try:
        stats = run_etl(file_path=archivo)
        df = stats.get('df_limpio')
        if df is not None:
            Patient.objects.all().delete()
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
                        bmi=float(row['IMC']) if pd.notna(row['IMC']) else None,
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
            'estado': 'exitoso', 'log_id': log.pk,
            'registros_extraidos':   log.registros_extraidos,
            'registros_duplicados':  log.registros_duplicados,
            'registros_nulos':       log.registros_nulos,
            'registros_fuera_rango': log.registros_fuera_rango,
            'generos_corregidos':    stats.get('generos_corregidos', 0),
            'registros_cargados':    log.registros_cargados,
            'tiempo_ejecucion':      log.tiempo_ejecucion,
            'mensaje':               log.mensaje,
        })
    except Exception as e:
        log.estado = 'fallido'; log.mensaje = str(e)
        log.fecha_fin = datetime.now(timezone.utc); log.save()
        return Response({'estado': 'fallido', 'log_id': log.pk, 'mensaje': str(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(tags=['ETL'], summary='Historial de ejecuciones ETL',
               description='Acceso: Analista y Administrador.')
@api_view(['GET'])
@permission_classes([IsAnalista])
def etl_historial(request):
    logs = ETLLog.objects.all()[:50]
    return Response(ETLLogSerializer(logs, many=True).data)


@extend_schema(tags=['ETL'], summary='Detalle de una ejecución ETL')
@api_view(['GET'])
@permission_classes([IsAnalista])
def etl_detalle(request, pk):
    try:
        log = ETLLog.objects.get(pk=pk)
    except ETLLog.DoesNotExist:
        return Response({'error': 'Log no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
    return Response(ETLLogSerializer(log).data)


# ── REPORTE DE CALIDAD DE DATOS ────────────────────────────────
@extend_schema(
    tags=['ETL'],
    summary='Reporte de calidad de datos del dataset original',
    description=(
        'Analiza el dataset original y muestra qué valores no numéricos o atípicos '
        'se encontraron en cada columna clínica, permitiendo al médico verificar '
        'que las correcciones del ETL fueron adecuadas.'
    ),
)
@api_view(['GET'])
@permission_classes([IsMedicoOrAnalista])
def data_quality_report(request):
    archivo = request.query_params.get('archivo', 'datasets/dataset_clinico_etl_1800_registros.xlsx')
    try:
        if archivo.endswith('.xlsx') or archivo.endswith('.xls'):
            df = pd.read_excel(archivo)
        else:
            df = pd.read_csv(archivo)
    except Exception as e:
        return Response({'error': f'No se pudo leer el archivo: {e}'}, status=400)

    columnas_clinicas = [
        'edad', 'peso', 'altura', 'IMC',
        'presión_sistólica', 'presión_diastólica',
        'frecuencia_cardiaca', 'glucosa', 'colesterol',
        'saturación_oxígeno', 'temperatura',
    ]

    reporte = {
        'total_registros': len(df),
        'archivo': archivo,
        'columnas': [],
        'resumen': {
            'valores_no_numericos': 0,
            'valores_nulos': 0,
            'valores_fuera_rango': 0,
        },
    }

    rangos_clinicos = {
        'presión_sistólica':      (60, 250),
        'presión_diastólica':     (30, 150),
        'frecuencia_cardiaca':    (30, 220),
        'glucosa':                (20, 600),
        'colesterol':             (50, 500),
        'saturación_oxígeno':     (50, 100),
        'temperatura':            (34, 42),
        'peso':                   (30, 300),
        'edad':                   (0, 120),
        'IMC':                    (10, 60),
        'altura':                 (1.0, 2.5),
    }

    total_no_numericos = 0
    total_nulos = 0
    total_fuera_rango = 0

    for col in columnas_clinicas:
        if col not in df.columns:
            continue

        original = df[col].copy()
        valores_originales = original.dropna().tolist()

        # Detectar valores no numéricos (texto)
        numericos = pd.to_numeric(original, errors='coerce')
        mask_no_numerico = original.notna() & numericos.isna()
        valores_texto = original[mask_no_numerico].unique().tolist()
        count_no_numericos = int(mask_no_numerico.sum())

        # Contar nulos originales
        count_nulos = int(original.isna().sum())

        # Valores fuera de rango (sobre los que sí son numéricos)
        rango = rangos_clinicos.get(col)
        count_fuera_rango = 0
        valores_fuera_rango = []
        if rango:
            mask_fr = (numericos.notna()) & ((numericos < rango[0]) | (numericos > rango[1]))
            count_fuera_rango = int(mask_fr.sum())
            if count_fuera_rango > 0:
                vals = numericos[mask_fr].dropna().unique().tolist()
                valores_fuera_rango = [round(float(v), 2) for v in vals[:10]]

        total_no_numericos += count_no_numericos
        total_nulos += count_nulos
        total_fuera_rango += count_fuera_rango

        # Mostrar ejemplos de valores no numéricos con contexto
        ejemplos_texto = []
        if count_no_numericos > 0:
            idxs = original[mask_no_numerico].index[:5]
            for idx in idxs:
                row_data = df.loc[idx]
                ejemplos_texto.append({
                    'fila': int(idx) + 2,
                    'valor_original': str(original[idx]),
                    'paciente': f"{row_data.get('nombres', '')} {row_data.get('apellidos', '')}",
                })

        col_info = {
            'nombre': col.replace('_', ' ').replace('presión', 'Presión').title(),
            'columna': col,
            'valores_no_numericos': count_no_numericos,
            'valores_texto_encontrados': [str(v) for v in valores_texto],
            'ejemplos': ejemplos_texto,
            'valores_nulos': count_nulos,
            'valores_fuera_rango': count_fuera_rango,
            'ejemplos_fuera_rango': valores_fuera_rango,
            'rango_esperado': f"{rangos_clinicos.get(col, ('N/A', 'N/A'))[0]} - {rangos_clinicos.get(col, ('N/A', 'N/A'))[1]}" if col in rangos_clinicos else 'N/A',
        }
        reporte['columnas'].append(col_info)

    reporte['resumen']['valores_no_numericos'] = total_no_numericos
    reporte['resumen']['valores_nulos'] = total_nulos
    reporte['resumen']['valores_fuera_rango'] = total_fuera_rango
    reporte['resumen']['total_anomalias'] = total_no_numericos + total_nulos + total_fuera_rango

    return Response(reporte)