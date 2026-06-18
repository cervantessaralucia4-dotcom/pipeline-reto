import pandas as pd
from django.db.models import Avg, Count, Q
import statistics
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.http import HttpResponse
from authentication.permissions import IsAnalista, IsMedicoOrAnalista
from patients.models import Patient
from patients.serializers import PatientSerializer
import csv
import io


@extend_schema(tags=['Analytics'], summary='Estadística descriptiva',
               description='Media, mediana, moda, desv. estándar de 9 variables. Acceso: Médico, Analista y Administrador.')
@api_view(['GET'])
@permission_classes([IsMedicoOrAnalista])
def estadisticas_descriptivas(request):
    pacientes = list(Patient.objects.all().values(
        'glucose', 'bmi', 'age', 'systolic_pressure', 'diastolic_pressure',
        'heart_rate', 'cholesterol', 'temperature', 'oxygen_saturation'
    ))
    
    campos = {
        'glucosa': 'glucose', 'imc': 'bmi', 'edad': 'age',
        'presion_sistolica': 'systolic_pressure', 'presion_diastolica': 'diastolic_pressure',
        'frecuencia_cardiaca': 'heart_rate', 'colesterol': 'cholesterol',
        'temperatura': 'temperature', 'saturacion_oxigeno': 'oxygen_saturation',
    }
    
    if not pacientes:
        return Response({k: {} for k in campos.keys()})
        
    df = pd.DataFrame(pacientes)
    resultado = {}
    
    for nombre, col in campos.items():
        if col not in df.columns or df[col].isnull().all():
            resultado[nombre] = {}
            continue
            
        serie = df[col].dropna()
        try:
            moda = float(serie.round().mode()[0]) if not serie.empty else None
        except Exception:
            moda = None
            
        resultado[nombre] = {
            'media': round(float(serie.mean()), 2),
            'mediana': round(float(serie.median()), 2),
            'moda': moda,
            'desviacion_estandar': round(float(serie.std(ddof=0)), 2) if len(serie) > 1 else 0.0,
            'minimo': round(float(serie.min()), 2),
            'maximo': round(float(serie.max()), 2),
            'n': int(serie.count()),
        }
    return Response(resultado)


@extend_schema(tags=['Analytics'], summary='KPIs médicos extendidos',
               description='Hipertensos, diabéticos, fumadores, obesidad. Acceso: Médico, Analista y Administrador.')
@api_view(['GET'])
@permission_classes([IsMedicoOrAnalista])
def kpis_medicos(request):
    kpis = Patient.objects.aggregate(
        total=Count('id'),
        hipertensos=Count('id', filter=Q(systolic_pressure__gte=140) | Q(diastolic_pressure__gte=90)),
        normotensos=Count('id', filter=Q(systolic_pressure__lt=120) & Q(diastolic_pressure__lt=80)),
        prehipertensos=Count('id', filter=(Q(systolic_pressure__gte=120) & Q(systolic_pressure__lt=140)) |
                             (Q(diastolic_pressure__gte=80) & Q(diastolic_pressure__lt=90))),
        diabeticos=Count('id', filter=Q(glucose__gt=126)),
        fumadores=Count('id', filter=Q(smoker=True)),
        con_antec=Count('id', filter=Q(family_history=True)),
        alcohol=Count('id', filter=Q(alcohol_consumption=True)),
        obesidad=Count('id', filter=Q(bmi__gte=30)),
        sat_baja=Count('id', filter=Q(oxygen_saturation__lt=90)),
        avg_glucosa=Avg('glucose'),
        avg_bmi=Avg('bmi'),
        avg_edad=Avg('age'),
        avg_colesterol=Avg('cholesterol'),
        avg_pres_sis=Avg('systolic_pressure')
    )
    
    total = kpis['total'] or 0
    if total == 0:
        return Response({'error': 'No hay pacientes registrados.'})
        
    def pct(n): return round((n / total) * 100, 1)
    
    return Response({
        'total_pacientes': total,
        'hipertensos':     {'cantidad': kpis['hipertensos'],     'porcentaje': pct(kpis['hipertensos'])},
        'normotensos':     {'cantidad': kpis['normotensos'],     'porcentaje': pct(kpis['normotensos'])},
        'prehipertensos':  {'cantidad': kpis['prehipertensos'],  'porcentaje': pct(kpis['prehipertensos'])},
        'diabeticos':      {'cantidad': kpis['diabeticos'],      'porcentaje': pct(kpis['diabeticos'])},
        'fumadores':       {'cantidad': kpis['fumadores'],   'porcentaje': pct(kpis['fumadores'])},
        'con_antecedentes':{'cantidad': kpis['con_antec'],   'porcentaje': pct(kpis['con_antec'])},
        'alcoholismo':     {'cantidad': kpis['alcohol'],     'porcentaje': pct(kpis['alcohol'])},
        'obesidad':        {'cantidad': kpis['obesidad'],    'porcentaje': pct(kpis['obesidad'])},
        'saturacion_baja': {'cantidad': kpis['sat_baja'],    'porcentaje': pct(kpis['sat_baja'])},
        'promedios': {
            'glucosa': round(kpis['avg_glucosa'] or 0, 2), 
            'imc': round(kpis['avg_bmi'] or 0, 2),
            'edad': round(kpis['avg_edad'] or 0, 1), 
            'colesterol': round(kpis['avg_colesterol'] or 0, 2),
            'presion_sistolica': round(kpis['avg_pres_sis'] or 0, 1),
        },
    })


@extend_schema(tags=['Analytics'], summary='Segmentación de pacientes',
               description='Por riesgo, sexo, diagnóstico, edad e IMC. Acceso: Médico, Analista y Administrador.')
@api_view(['GET'])
@permission_classes([IsMedicoOrAnalista])
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


@extend_schema(tags=['Analytics'], summary='Detección de pacientes críticos',
               description='Presión > 180, glucosa > 300, saturación < 85. Acceso: Médico, Analista y Administrador.')
@api_view(['GET'])
@permission_classes([IsMedicoOrAnalista])
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


FILTROS_CONDICION = {
    'hipertensos':      Q(systolic_pressure__gte=140) | Q(diastolic_pressure__gte=90),
    'normotensos':      Q(systolic_pressure__lt=120) & Q(diastolic_pressure__lt=80),
    'prehipertensos':   Q(systolic_pressure__gte=120, systolic_pressure__lt=140) |
                        Q(diastolic_pressure__gte=80, diastolic_pressure__lt=90),
    'diabeticos':       Q(glucose__gt=126),
    'fumadores':        Q(smoker=True),
    'con_antecedentes': Q(family_history=True),
    'alcoholismo':      Q(alcohol_consumption=True),
    'obesidad':         Q(bmi__gte=30),
    'saturacion_baja':  Q(oxygen_saturation__lt=90),
}

FILTROS_ETIQUETA = {
    'hipertensos':      'Hipertensos',
    'normotensos':      'Normotensos',
    'prehipertensos':   'Prehipertensos',
    'diabeticos':       'Diabéticos',
    'fumadores':        'Fumadores',
    'con_antecedentes': 'Con antecedentes',
    'alcoholismo':      'Alcoholismo',
    'obesidad':         'Obesidad',
    'saturacion_baja':  'Saturación baja',
}


@extend_schema(tags=['Analytics'], summary='Pacientes por filtro médico',
               description='Retorna pacientes que cumplen una condición: hipertensos, diabeticos, fumadores, etc.')
@api_view(['GET'])
@permission_classes([IsMedicoOrAnalista])
def pacientes_por_filtro(request):
    filtro = request.query_params.get('filtro', '')
    condicion = FILTROS_CONDICION.get(filtro)
    if not condicion:
        return Response({'error': f'Filtro inválido. Opciones: {", ".join(FILTROS_CONDICION.keys())}'},
                        status=400)
    pacientes = Patient.objects.filter(condicion).order_by('id')
    serializer = PatientSerializer(pacientes, many=True)
    return Response({
        'filtro': filtro,
        'etiqueta': FILTROS_ETIQUETA.get(filtro, filtro),
        'total': pacientes.count(),
        'pacientes': serializer.data,
    })


# ── EXPORTAR CSV POR FILTRO ────────────────────────────────────
@extend_schema(tags=['Analytics'], summary='Exportar filtro a CSV',
               description='Descarga CSV con pacientes de un filtro específico.')
@api_view(['GET'])
@permission_classes([IsMedicoOrAnalista])
def export_filtro_csv(request):
    filtro = request.query_params.get('filtro', '')
    condicion = FILTROS_CONDICION.get(filtro)
    etiqueta = FILTROS_ETIQUETA.get(filtro, filtro)
    if not condicion:
        return HttpResponse('Filtro inválido', status=400)

    pacientes = Patient.objects.filter(condicion).order_by('id')
    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = f'attachment; filename="{filtro}.csv"'
    response.write('\ufeff')
    writer = csv.writer(response)
    writer.writerow(['ID', 'Nombre', 'Apellido', 'Edad', 'Sexo', 'Peso', 'Altura',
                     'IMC', 'Presión Sistólica', 'Presión Diastólica',
                     'Frecuencia Cardíaca', 'Glucosa', 'Colesterol',
                     'Saturación O₂', 'Temperatura', 'Antecedentes Familiares',
                     'Fumador', 'Consumo Alcohol', 'Actividad Física',
                     'Diagnóstico Preliminar', 'Riesgo', 'Fecha Consulta'])
    campos = ['id', 'first_name', 'last_name', 'age', 'sex', 'weight', 'height',
              'bmi', 'systolic_pressure', 'diastolic_pressure', 'heart_rate',
              'glucose', 'cholesterol', 'oxygen_saturation', 'temperature',
              'family_history', 'smoker', 'alcohol_consumption', 'physical_activity',
              'preliminary_diagnosis', 'disease_risk', 'consultation_date']
    for p in pacientes.values_list(*campos):
        writer.writerow(p)
    return response


# ── EXPORTAR PDF POR FILTRO ────────────────────────────────────
@extend_schema(tags=['Analytics'], summary='Exportar filtro a PDF',
               description='Descarga PDF con pacientes de un filtro específico.')
@api_view(['GET'])
@permission_classes([IsMedicoOrAnalista])
def export_filtro_pdf(request):
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.units import mm
    from reportlab.lib.enums import TA_CENTER

    filtro = request.query_params.get('filtro', '')
    condicion = FILTROS_CONDICION.get(filtro)
    etiqueta = FILTROS_ETIQUETA.get(filtro, filtro)
    if not condicion:
        return HttpResponse('Filtro inválido', status=400)

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4),
                            topMargin=12*mm, bottomMargin=12*mm,
                            leftMargin=8*mm, rightMargin=8*mm)
    styles = getSampleStyleSheet()
    elements = []

    title_style = ParagraphStyle('Title2', parent=styles['Title'],
                                  fontSize=16, spaceAfter=4, textColor=colors.HexColor('#1F4E79'))
    elements.append(Paragraph(f'Pacientes: {etiqueta}', title_style))
    elements.append(Spacer(1, 3*mm))

    pacientes = Patient.objects.filter(condicion).order_by('id')
    data = [['ID', 'Nombre', 'Edad', 'Sexo', 'P. Sist', 'P. Diast',
             'FC', 'Glucosa', 'Colesterol', 'Sat O₂', 'Temp', 'IMC', 'Riesgo']]
    for p in pacientes:
        data.append([
            str(p.id), f"{p.first_name} {p.last_name}", str(p.age),
            p.sex, str(p.systolic_pressure or ''), str(p.diastolic_pressure or ''),
            str(p.heart_rate or ''), str(p.glucose or ''), str(p.cholesterol or ''),
            str(p.oxygen_saturation or ''), str(p.temperature or ''),
            str(p.bmi or ''), p.disease_risk
        ])

    col_widths = [25, 80, 25, 25, 30, 30, 28, 35, 35, 30, 28, 28, 40]
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1F4E79')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 7),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F2F7FB')]),
        ('FONTSIZE', (0, 1), (-1, -1), 6.5),
    ]))
    elements.append(t)

    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filtro}.pdf"'
    return response