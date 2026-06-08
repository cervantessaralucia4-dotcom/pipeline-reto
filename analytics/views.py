from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Avg, Max, Min, Count, StdDev
import statistics
from patients.models import Patient


def _lista(campo):
    return list(Patient.objects.exclude(**{f"{campo}__isnull": True}).values_list(campo, flat=True))


@extend_schema(
    tags=['Analytics'],
    summary='Estadística descriptiva de variables clínicas',
    description='Retorna media, mediana, moda, desviación estándar, mínimo y máximo de 9 variables clínicas.',
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def estadisticas_descriptivas(request):
    campos = {
        'glucosa': 'glucose', 'imc': 'bmi', 'edad': 'age',
        'presion_sistolica': 'systolic_pressure', 'presion_diastolica': 'diastolic_pressure',
        'frecuencia_cardiaca': 'heart_rate', 'colesterol': 'cholesterol',
        'temperatura': 'temperature', 'saturacion_oxigeno': 'oxygen_saturation',
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
            media=Avg(campo), maximo=Max(campo), minimo=Min(campo), desviacion=StdDev(campo),
        )
        resultado[nombre] = {
            'media':              round(agg['media'] or 0, 2),
            'mediana':            round(statistics.median(valores), 2),
            'moda':               moda,
            'desviacion_estandar':round(agg['desviacion'] or 0, 2),
            'minimo':             round(agg['minimo'] or 0, 2),
            'maximo':             round(agg['maximo'] or 0, 2),
            'n':                  len(valores),
        }
    return Response(resultado)


@extend_schema(
    tags=['Analytics'],
    summary='KPIs médicos extendidos',
    description='Hipertensos, diabéticos, fumadores, obesidad, saturación baja y promedios clínicos con porcentajes.',
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def kpis_medicos(request):
    total = Patient.objects.count()
    if total == 0:
        return Response({'error': 'No hay pacientes registrados.'})
    def pct(n): return round((n / total) * 100, 1) if total else 0

    hipertensos = Patient.objects.filter(systolic_pressure__gt=140).count()
    diabeticos  = Patient.objects.filter(glucose__gt=126).count()
    fumadores   = Patient.objects.filter(smoker=True).count()
    con_antec   = Patient.objects.filter(family_history=True).count()
    alcoholismo = Patient.objects.filter(alcohol_consumption=True).count()
    obesidad    = Patient.objects.filter(bmi__gte=30).count()
    sat_baja    = Patient.objects.filter(oxygen_saturation__lt=90).count()
    agg = Patient.objects.aggregate(
        avg_gluc=Avg('glucose'), avg_bmi=Avg('bmi'), avg_edad=Avg('age'),
        avg_colesterol=Avg('cholesterol'), avg_pres_sis=Avg('systolic_pressure'),
    )
    return Response({
        'total_pacientes':   total,
        'hipertensos':       {'cantidad': hipertensos,  'porcentaje': pct(hipertensos)},
        'diabeticos':        {'cantidad': diabeticos,   'porcentaje': pct(diabeticos)},
        'fumadores':         {'cantidad': fumadores,    'porcentaje': pct(fumadores)},
        'con_antecedentes':  {'cantidad': con_antec,    'porcentaje': pct(con_antec)},
        'alcoholismo':       {'cantidad': alcoholismo,  'porcentaje': pct(alcoholismo)},
        'obesidad':          {'cantidad': obesidad,     'porcentaje': pct(obesidad)},
        'saturacion_baja':   {'cantidad': sat_baja,     'porcentaje': pct(sat_baja)},
        'promedios': {
            'glucosa':           round(agg['avg_gluc']       or 0, 2),
            'imc':               round(agg['avg_bmi']        or 0, 2),
            'edad':              round(agg['avg_edad']       or 0, 1),
            'colesterol':        round(agg['avg_colesterol'] or 0, 2),
            'presion_sistolica': round(agg['avg_pres_sis']   or 0, 1),
        },
    })


@extend_schema(
    tags=['Analytics'],
    summary='Segmentación de pacientes',
    description='Segmentación por riesgo, sexo, diagnóstico, grupo etario y clasificación IMC.',
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def segmentacion(request):
    return Response({
        'por_riesgo':      list(Patient.objects.values('disease_risk').annotate(cantidad=Count('id')).order_by('-cantidad')),
        'por_sexo':        list(Patient.objects.values('sex').annotate(cantidad=Count('id'))),
        'por_diagnostico': list(Patient.objects.values('preliminary_diagnosis').annotate(cantidad=Count('id')).order_by('-cantidad')[:10]),
        'por_actividad':   list(Patient.objects.values('physical_activity').annotate(cantidad=Count('id'))),
        'por_grupo_edad': {
            '0-17':  Patient.objects.filter(age__lt=18).count(),
            '18-35': Patient.objects.filter(age__gte=18, age__lte=35).count(),
            '36-50': Patient.objects.filter(age__gte=36, age__lte=50).count(),
            '51-65': Patient.objects.filter(age__gte=51, age__lte=65).count(),
            '65+':   Patient.objects.filter(age__gt=65).count(),
        },
        'por_imc': {
            'bajo_peso': Patient.objects.filter(bmi__lt=18.5).count(),
            'normal':    Patient.objects.filter(bmi__gte=18.5, bmi__lt=25).count(),
            'sobrepeso': Patient.objects.filter(bmi__gte=25, bmi__lt=30).count(),
            'obesidad':  Patient.objects.filter(bmi__gte=30).count(),
        },
    })


@extend_schema(
    tags=['Analytics'],
    summary='Detección de pacientes críticos',
    description='Detecta pacientes críticos por presión sistólica > 180, glucosa > 300 o saturación < 85.',
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pacientes_criticos(request):
    criticos = Patient.objects.filter(disease_risk='Crítico').values(
        'id','first_name','last_name','age','sex',
        'glucose','systolic_pressure','oxygen_saturation',
        'bmi','disease_risk','preliminary_diagnosis'
    ).order_by('-glucose')[:50]
    return Response({
        'total_criticos': Patient.objects.filter(disease_risk='Crítico').count(),
        'alertas': {
            'presion_sistolica_gt_180': Patient.objects.filter(systolic_pressure__gt=180).count(),
            'glucosa_gt_300':           Patient.objects.filter(glucose__gt=300).count(),
            'saturacion_lt_85':         Patient.objects.filter(oxygen_saturation__lt=85).count(),
        },
        'pacientes': list(criticos),
    })