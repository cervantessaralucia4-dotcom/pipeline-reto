# ═══════════════════════════════════════════════════════════════
#  patients/views.py
# ═══════════════════════════════════════════════════════════════
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Avg

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
    total   = Patient.objects.count()
    critico = Patient.objects.filter(disease_risk='Crítico').count()
    alto    = Patient.objects.filter(disease_risk='Alto').count()
    medio   = Patient.objects.filter(disease_risk='Medio').count()
    bajo    = Patient.objects.filter(disease_risk='Bajo').count()
    avg_gluc = Patient.objects.aggregate(Avg('glucose'))['glucose__avg'] or 0
    avg_bmi  = Patient.objects.aggregate(Avg('bmi'))['bmi__avg'] or 0

    return Response({
        'total_patients':    total,
        'critical_patients': critico,
        'high_risk':         alto,
        'medium_risk':       medio,
        'low_risk':          bajo,
        'average_glucose':   round(avg_gluc, 2),
        'average_bmi':       round(avg_bmi,  2),
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
    return Response({
        'risk_distribution': {
            'Crítico': Patient.objects.filter(disease_risk='Crítico').count(),
            'Alto':    Patient.objects.filter(disease_risk='Alto').count(),
            'Medio':   Patient.objects.filter(disease_risk='Medio').count(),
            'Bajo':    Patient.objects.filter(disease_risk='Bajo').count(),
        },
        'gender_distribution': {
            'Masculino': Patient.objects.filter(sex='M').count(),
            'Femenino':  Patient.objects.filter(sex='F').count(),
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
    avg_gluc = Patient.objects.aggregate(Avg('glucose'))['glucose__avg'] or 0
    avg_bmi  = Patient.objects.aggregate(Avg('bmi'))['bmi__avg'] or 0
    return Response({
        'total_patients':    Patient.objects.count(),
        'critical_patients': Patient.objects.filter(disease_risk='Crítico').count(),
        'average_glucose':   round(avg_gluc, 2),
        'average_bmi':       round(avg_bmi, 2),
        'risk_distribution': {
            'Crítico': Patient.objects.filter(disease_risk='Crítico').count(),
            'Alto':    Patient.objects.filter(disease_risk='Alto').count(),
            'Medio':   Patient.objects.filter(disease_risk='Medio').count(),
            'Bajo':    Patient.objects.filter(disease_risk='Bajo').count(),
        },
    })