# ═══════════════════════════════════════════════════════════════
#  analytics/views.py
#  Endpoints:
#    GET /api/analytics/estadisticas/   — estadística descriptiva
#    GET /api/analytics/kpis/           — KPIs médicos extendidos
#    GET /api/analytics/segmentacion/   — segmentación de pacientes
#    GET /api/analytics/criticos/       — detección de críticos
# ═══════════════════════════════════════════════════════════════
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.db.models import Avg, Max, Min, Count, StdDev

import statistics

from patients.models import Patient


def _lista(campo):
    """Retorna lista de valores no nulos de un campo numérico."""
    return list(
        Patient.objects.exclude(**{f"{campo}__isnull": True})
                       .values_list(campo, flat=True)
    )


# ── GET /api/analytics/estadisticas/ ─────────────────────────
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def estadisticas_descriptivas(request):
    """
    Estadística descriptiva completa de variables clínicas:
    media, mediana, moda, desviación estándar, mín y máx.
    """
    campos = {
        'glucosa':            'glucose',
        'imc':                'bmi',
        'edad':               'age',
        'presion_sistolica':  'systolic_pressure',
        'presion_diastolica': 'diastolic_pressure',
        'frecuencia_cardiaca': 'heart_rate',
        'colesterol':         'cholesterol',
        'temperatura':        'temperature',
        'saturacion_oxigeno': 'oxygen_saturation',
    }

    resultado = {}

    for nombre, campo in campos.items():
        valores = _lista(campo)
        if not valores:
            resultado[nombre] = {}
            continue

        try:
            moda = statistics.mode(round(v) for v in valores)
        except statistics.StatisticsError:
            moda = None

        agg = Patient.objects.aggregate(
            media=Avg(campo),
            maximo=Max(campo),
            minimo=Min(campo),
            desviacion=StdDev(campo),
        )

        resultado[nombre] = {
            'media':     round(agg['media'] or 0, 2),
            'mediana':   round(statistics.median(valores), 2),
            'moda':      moda,
            'desviacion_estandar': round(agg['desviacion'] or 0, 2),
            'minimo':    round(agg['minimo'] or 0, 2),
            'maximo':    round(agg['maximo'] or 0, 2),
            'n':         len(valores),
        }

    return Response(resultado)


# ── GET /api/analytics/kpis/ ─────────────────────────────────
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def kpis_medicos(request):
    """
    KPIs médicos extendidos: hipertensos, diabéticos,
    fumadores, con antecedentes y promedios clínicos.
    """
    total = Patient.objects.count()
    if total == 0:
        return Response({'error': 'No hay pacientes registrados.'})

    def pct(n):
        return round((n / total) * 100, 1) if total else 0

    # Conteos clínicos
    hipertensos  = Patient.objects.filter(systolic_pressure__gt=140).count()
    diabeticos   = Patient.objects.filter(glucose__gt=126).count()
    fumadores    = Patient.objects.filter(smoker=True).count()
    con_antec    = Patient.objects.filter(family_history=True).count()
    alcoholismo  = Patient.objects.filter(alcohol_consumption=True).count()
    obesidad     = Patient.objects.filter(bmi__gte=30).count()
    sat_baja     = Patient.objects.filter(oxygen_saturation__lt=90).count()

    # Promedios
    agg = Patient.objects.aggregate(
        avg_gluc=Avg('glucose'),
        avg_bmi=Avg('bmi'),
        avg_edad=Avg('age'),
        avg_colesterol=Avg('cholesterol'),
        avg_pres_sis=Avg('systolic_pressure'),
    )

    return Response({
        'total_pacientes': total,

        # Indicadores de riesgo
        'hipertensos':     {'cantidad': hipertensos,  'porcentaje': pct(hipertensos)},
        'diabeticos':      {'cantidad': diabeticos,   'porcentaje': pct(diabeticos)},
        'fumadores':       {'cantidad': fumadores,    'porcentaje': pct(fumadores)},
        'con_antecedentes':{'cantidad': con_antec,    'porcentaje': pct(con_antec)},
        'alcoholismo':     {'cantidad': alcoholismo,  'porcentaje': pct(alcoholismo)},
        'obesidad':        {'cantidad': obesidad,     'porcentaje': pct(obesidad)},
        'saturacion_baja': {'cantidad': sat_baja,     'porcentaje': pct(sat_baja)},

        # Promedios generales
        'promedios': {
            'glucosa':            round(agg['avg_gluc']      or 0, 2),
            'imc':                round(agg['avg_bmi']       or 0, 2),
            'edad':               round(agg['avg_edad']      or 0, 1),
            'colesterol':         round(agg['avg_colesterol'] or 0, 2),
            'presion_sistolica':  round(agg['avg_pres_sis']  or 0, 1),
        },
    })


# ── GET /api/analytics/segmentacion/ ─────────────────────────
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def segmentacion(request):
    """
    Segmentación de pacientes por edad, sexo, riesgo,
    diagnóstico, IMC y actividad física.
    """
    # Por riesgo
    por_riesgo = list(
        Patient.objects.values('disease_risk')
                       .annotate(cantidad=Count('id'))
                       .order_by('-cantidad')
    )

    # Por sexo
    por_sexo = list(
        Patient.objects.values('sex')
                       .annotate(cantidad=Count('id'))
    )

    # Por diagnóstico
    por_diagnostico = list(
        Patient.objects.values('preliminary_diagnosis')
                       .annotate(cantidad=Count('id'))
                       .order_by('-cantidad')[:10]
    )

    # Por actividad física
    por_actividad = list(
        Patient.objects.values('physical_activity')
                       .annotate(cantidad=Count('id'))
    )

    # Por grupo etario
    total = Patient.objects.count()
    grupos_edad = {
        '0-17':  Patient.objects.filter(age__lt=18).count(),
        '18-35': Patient.objects.filter(age__gte=18, age__lte=35).count(),
        '36-50': Patient.objects.filter(age__gte=36, age__lte=50).count(),
        '51-65': Patient.objects.filter(age__gte=51, age__lte=65).count(),
        '65+':   Patient.objects.filter(age__gt=65).count(),
    }

    # Por clasificación IMC
    imc_grupos = {
        'bajo_peso':   Patient.objects.filter(bmi__lt=18.5).count(),
        'normal':      Patient.objects.filter(bmi__gte=18.5, bmi__lt=25).count(),
        'sobrepeso':   Patient.objects.filter(bmi__gte=25, bmi__lt=30).count(),
        'obesidad':    Patient.objects.filter(bmi__gte=30).count(),
    }

    return Response({
        'por_riesgo':      por_riesgo,
        'por_sexo':        por_sexo,
        'por_diagnostico': por_diagnostico,
        'por_actividad':   por_actividad,
        'por_grupo_edad':  grupos_edad,
        'por_imc':         imc_grupos,
    })


# ── GET /api/analytics/criticos/ ─────────────────────────────
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pacientes_criticos(request):
    """
    Detecta pacientes críticos según reglas clínicas:
    presión sistólica > 180, glucosa > 300, saturación < 85.
    """
    criticos = Patient.objects.filter(
        disease_risk='Crítico'
    ).values(
        'id', 'first_name', 'last_name', 'age', 'sex',
        'glucose', 'systolic_pressure', 'oxygen_saturation',
        'bmi', 'disease_risk', 'preliminary_diagnosis'
    ).order_by('-glucose')[:50]

    # Alertas específicas por regla clínica
    pres_alta  = Patient.objects.filter(systolic_pressure__gt=180).count()
    gluc_alta  = Patient.objects.filter(glucose__gt=300).count()
    sat_baja   = Patient.objects.filter(oxygen_saturation__lt=85).count()

    return Response({
        'total_criticos': Patient.objects.filter(disease_risk='Crítico').count(),
        'alertas': {
            'presion_sistolica_gt_180': pres_alta,
            'glucosa_gt_300':           gluc_alta,
            'saturacion_lt_85':         sat_baja,
        },
        'pacientes': list(criticos),
    })