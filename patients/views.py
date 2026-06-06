from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg

from .models import Patient
from .serializers import PatientSerializer
from .predict import predict_risk


# ── PACIENTES CRUD ───────────────────────────────────────────
class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]


# ── PREDICCIÓN ML ────────────────────────────────────────────
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def predict_view(request):
    prediction = predict_risk(request.data)
    return Response({'prediction': prediction})


# ── DASHBOARD KPIs ───────────────────────────────────────────
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_kpis(request):
    total    = Patient.objects.count()
    critico  = Patient.objects.filter(disease_risk='Crítico').count()
    alto     = Patient.objects.filter(disease_risk='Alto').count()
    medio    = Patient.objects.filter(disease_risk='Medio').count()
    bajo     = Patient.objects.filter(disease_risk='Bajo').count()
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
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def reports_view(request):
    avg_gluc = Patient.objects.aggregate(Avg('glucose'))['glucose__avg'] or 0
    avg_bmi  = Patient.objects.aggregate(Avg('bmi'))['bmi__avg'] or 0
    return Response({
        'total_patients':    Patient.objects.count(),
        'critical_patients': Patient.objects.filter(disease_risk='Crítico').count(),
        'average_glucose':   round(avg_gluc, 2),
        'average_bmi':       round(avg_bmi,  2),
        'risk_distribution': {
            'Crítico': Patient.objects.filter(disease_risk='Crítico').count(),
            'Alto':    Patient.objects.filter(disease_risk='Alto').count(),
            'Medio':   Patient.objects.filter(disease_risk='Medio').count(),
            'Bajo':    Patient.objects.filter(disease_risk='Bajo').count(),
        },
    })