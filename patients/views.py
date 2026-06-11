# ═══════════════════════════════════════════════════════════════
#  patients/views.py
# ═══════════════════════════════════════════════════════════════
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Avg, Count, Q
from django.http import HttpResponse
import csv

from authentication.permissions import IsAdministrador, IsMedicoOrAnalista
from .models import Patient
from .serializers import PatientSerializer
from .predict import predict_risk


# ── PACIENTES CRUD ───────────────────────────────────────────
@extend_schema(tags=['Pacientes'])
class PatientViewSet(viewsets.ModelViewSet):
    """
    CRUD completo de pacientes clínicos.
    - GET    /api/patients/        — listar (Médico, Analista, Admin)
    - POST   /api/patients/        — crear  (solo Admin)
    - GET    /api/patients/{id}/   — detalle (Médico, Analista, Admin)
    - PUT    /api/patients/{id}/   — actualizar (solo Admin)
    - DELETE /api/patients/{id}/   — eliminar (solo Admin)
    """
    queryset         = Patient.objects.all()
    serializer_class = PatientSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [IsMedicoOrAnalista()]
        return [IsAdministrador()]


# ── PREDICCIÓN ML ────────────────────────────────────────────
@extend_schema(
    tags=['Machine Learning'],
    summary='Predecir riesgo (acceso directo)',
    description='Alias de /api/ml/predict/. Acceso: Médico, Analista y Administrador.',
)
@api_view(['POST'])
@permission_classes([IsMedicoOrAnalista])
def predict_view(request):
    resultado = predict_risk(request.data)
    return Response({'prediction': resultado})


# ── DASHBOARD KPIs ───────────────────────────────────────────
@extend_schema(
    tags=['Dashboard'],
    summary='KPIs principales del dashboard',
    description='Total pacientes, críticos, riesgo alto/medio/bajo, glucosa e IMC promedio. Acceso: todos los roles.',
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_kpis(request):
    kpis = Patient.objects.aggregate(
        total=Count('id'),
        critico=Count('id', filter=Q(disease_risk='Crítico')),
        alto=Count('id', filter=Q(disease_risk='Alto')),
        medio=Count('id', filter=Q(disease_risk='Medio')),
        bajo=Count('id', filter=Q(disease_risk='Bajo')),
        avg_gluc=Avg('glucose'),
        avg_bmi=Avg('bmi')
    )

    return Response({
        'total_patients':    kpis['total'] or 0,
        'critical_patients': kpis['critico'] or 0,
        'high_risk':         kpis['alto'] or 0,
        'medium_risk':       kpis['medio'] or 0,
        'low_risk':          kpis['bajo'] or 0,
        'average_glucose':   round(kpis['avg_gluc'] or 0, 2),
        'average_bmi':       round(kpis['avg_bmi'] or 0, 2),
    })


# ── DASHBOARD CHARTS ─────────────────────────────────────────
@extend_schema(
    tags=['Dashboard'],
    summary='Datos para gráficas del dashboard',
    description='Distribución por riesgo y sexo. Acceso: todos los roles.',
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_charts(request):
    dist = Patient.objects.aggregate(
        critico=Count('id', filter=Q(disease_risk='Crítico')),
        alto=Count('id', filter=Q(disease_risk='Alto')),
        medio=Count('id', filter=Q(disease_risk='Medio')),
        bajo=Count('id', filter=Q(disease_risk='Bajo')),
        masc=Count('id', filter=Q(sex='M')),
        fem=Count('id', filter=Q(sex='F'))
    )
    return Response({
        'risk_distribution': {
            'Crítico': dist['critico'] or 0,
            'Alto':    dist['alto'] or 0,
            'Medio':   dist['medio'] or 0,
            'Bajo':    dist['bajo'] or 0,
        },
        'gender_distribution': {
            'Masculino': dist['masc'] or 0,
            'Femenino':  dist['fem'] or 0,
        },
    })


# ── REPORTES ─────────────────────────────────────────────────
@extend_schema(
    tags=['Reportes'],
    summary='Reporte general del sistema',
    description='Resumen ejecutivo con totales, promedios y distribución de riesgo. Acceso: todos los roles.',
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def reports_view(request):
    stats = Patient.objects.aggregate(
        total=Count('id'),
        critico=Count('id', filter=Q(disease_risk='Crítico')),
        alto=Count('id', filter=Q(disease_risk='Alto')),
        medio=Count('id', filter=Q(disease_risk='Medio')),
        bajo=Count('id', filter=Q(disease_risk='Bajo')),
        avg_gluc=Avg('glucose'),
        avg_bmi=Avg('bmi'),
    )
    return Response({
        'total_patients':    stats['total'] or 0,
        'critical_patients': stats['critico'] or 0,
        'average_glucose':   round(stats['avg_gluc'] or 0, 2),
        'average_bmi':       round(stats['avg_bmi'] or 0, 2),
        'risk_distribution': {
            'Crítico': stats['critico'] or 0,
            'Alto':    stats['alto'] or 0,
            'Medio':   stats['medio'] or 0,
            'Bajo':    stats['bajo'] or 0,
        },
    })


# ── EXPORTAR CSV ──────────────────────────────────────────────
@extend_schema(
    tags=['Reportes'],
    summary='Exportar pacientes a CSV',
    description='Descarga un archivo CSV con todos los pacientes. Acceso: Médico, Analista y Administrador.',
)
@api_view(['GET'])
@permission_classes([IsMedicoOrAnalista])
def export_csv_view(request):
    campos = [
        'id', 'first_name', 'last_name', 'age', 'sex', 'weight', 'height', 'bmi',
        'systolic_pressure', 'diastolic_pressure', 'heart_rate', 'glucose',
        'cholesterol', 'oxygen_saturation', 'temperature', 'family_history',
        'smoker', 'alcohol_consumption', 'physical_activity',
        'preliminary_diagnosis', 'disease_risk', 'consultation_date',
    ]
    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = 'attachment; filename="pacientes.csv"'
    response.write('\ufeff')
    writer = csv.writer(response)
    encabezados = ['ID', 'Nombre', 'Apellido', 'Edad', 'Sexo', 'Peso', 'Altura',
                   'IMC', 'Presión Sistólica', 'Presión Diastólica',
                   'Frecuencia Cardíaca', 'Glucosa', 'Colesterol',
                   'Saturación O₂', 'Temperatura', 'Antecedentes Familiares',
                   'Fumador', 'Consumo Alcohol', 'Actividad Física',
                   'Diagnóstico Preliminar', 'Riesgo', 'Fecha Consulta']
    writer.writerow(encabezados)
    for p in Patient.objects.all().values_list(*campos):
        writer.writerow(p)
    return response