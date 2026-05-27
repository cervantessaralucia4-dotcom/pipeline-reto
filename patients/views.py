from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.db.models import Avg

import subprocess

from .models import Patient
from .serializers import PatientSerializer

from .predict import predict_risk


# =========================
# VIEWSET PACIENTES
# =========================

class PatientViewSet(viewsets.ModelViewSet):

    queryset = Patient.objects.all()

    serializer_class = PatientSerializer

    permission_classes = [IsAuthenticated]


# =========================
# PREDICCIÓN IA
# =========================

@api_view(['POST'])
def predict_view(request):

    prediction = predict_risk(request.data)

    return Response({
        'prediction': prediction
    })


# =========================
# DASHBOARD KPIS
# =========================

@api_view(['GET'])
def dashboard_kpis(request):

    total_patients = Patient.objects.count()

    critical_patients = Patient.objects.filter(
        riesgo_calculado='Crítico'
    ).count()

    high_risk = Patient.objects.filter(
        riesgo_calculado='Alto'
    ).count()

    medium_risk = Patient.objects.filter(
        riesgo_calculado='Medio'
    ).count()

    low_risk = Patient.objects.filter(
        riesgo_calculado='Bajo'
    ).count()

    average_glucose = Patient.objects.aggregate(
        Avg('glucosa')
    )['glucosa__avg']

    average_bmi = Patient.objects.aggregate(
        Avg('IMC')
    )['IMC__avg']

    return Response({

        'total_patients': total_patients,

        'critical_patients': critical_patients,

        'high_risk': high_risk,

        'medium_risk': medium_risk,

        'low_risk': low_risk,

        'average_glucose': round(
            average_glucose,
            2
        ),

        'average_bmi': round(
            average_bmi,
            2
        )

    })


# =========================
# CHARTS API
# =========================

@api_view(['GET'])
def dashboard_charts(request):

    risk_distribution = {

        'Crítico': Patient.objects.filter(
            riesgo_calculado='Crítico'
        ).count(),

        'Alto': Patient.objects.filter(
            riesgo_calculado='Alto'
        ).count(),

        'Medio': Patient.objects.filter(
            riesgo_calculado='Medio'
        ).count(),

        'Bajo': Patient.objects.filter(
            riesgo_calculado='Bajo'
        ).count(),

    }

    return Response({

        'risk_distribution': risk_distribution

    })


# =========================
# REPORTES API
# =========================

@api_view(['GET'])
def reports_view(request):

    total_patients = Patient.objects.count()

    critical_patients = Patient.objects.filter(
        riesgo_calculado='Crítico'
    ).count()

    average_glucose = Patient.objects.aggregate(
        Avg('glucosa')
    )['glucosa__avg']

    average_bmi = Patient.objects.aggregate(
        Avg('IMC')
    )['IMC__avg']

    risk_distribution = {

        'Crítico': Patient.objects.filter(
            riesgo_calculado='Crítico'
        ).count(),

        'Alto': Patient.objects.filter(
            riesgo_calculado='Alto'
        ).count(),

        'Medio': Patient.objects.filter(
            riesgo_calculado='Medio'
        ).count(),

        'Bajo': Patient.objects.filter(
            riesgo_calculado='Bajo'
        ).count(),

    }

    return Response({

        'total_patients': total_patients,

        'critical_patients': critical_patients,

        'average_glucose': round(
            average_glucose,
            2
        ),

        'average_bmi': round(
            average_bmi,
            2
        ),

        'risk_distribution': risk_distribution

    })


# =========================
# ETL RUN API
# =========================

@api_view(['POST'])
def run_etl(request):

    try:

        subprocess.run(
            ['python', 'etl/etl_process.py'],
            check=True
        )

        return Response({

            'message': 'ETL ejecutado correctamente'

        })

    except Exception as e:

        return Response({

            'error': str(e)

        })