from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.db.models import Avg

import subprocess

from .models import Patient
from .serializers import PatientSerializer
from .predict import predict_risk


class PatientViewSet(viewsets.ModelViewSet):

    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]


@api_view(['POST'])
def predict_view(request):

    prediction = predict_risk(request.data)

    return Response({
        'prediction': prediction
    })


@api_view(['GET'])
def dashboard_kpis(request):

    total_patients = Patient.objects.count()

    critical_patients = Patient.objects.filter(
        disease_risk='Crítico'
    ).count()

    high_risk = Patient.objects.filter(
        disease_risk='Alto'
    ).count()

    medium_risk = Patient.objects.filter(
        disease_risk='Medio'
    ).count()

    low_risk = Patient.objects.filter(
        disease_risk='Bajo'
    ).count()

    average_glucose = Patient.objects.aggregate(
        Avg('glucose')
    )['glucose__avg'] or 0

    average_bmi = Patient.objects.aggregate(
        Avg('bmi')
    )['bmi__avg'] or 0

    return Response({

        'total_patients': total_patients,
        'critical_patients': critical_patients,
        'high_risk': high_risk,
        'medium_risk': medium_risk,
        'low_risk': low_risk,
        'average_glucose': round(average_glucose, 2),
        'average_bmi': round(average_bmi, 2)

    })


@api_view(['GET'])
def dashboard_charts(request):

    risk_distribution = {

        'Crítico': Patient.objects.filter(
            disease_risk='Crítico'
        ).count(),

        'Alto': Patient.objects.filter(
            disease_risk='Alto'
        ).count(),

        'Medio': Patient.objects.filter(
            disease_risk='Medio'
        ).count(),

        'Bajo': Patient.objects.filter(
            disease_risk='Bajo'
        ).count(),
    }

    return Response({
        'risk_distribution': risk_distribution
    })


@api_view(['GET'])
def reports_view(request):

    total_patients = Patient.objects.count()

    critical_patients = Patient.objects.filter(
        disease_risk='Crítico'
    ).count()

    average_glucose = Patient.objects.aggregate(
        Avg('glucose')
    )['glucose__avg'] or 0

    average_bmi = Patient.objects.aggregate(
        Avg('bmi')
    )['bmi__avg'] or 0

    risk_distribution = {

        'Crítico': Patient.objects.filter(
            disease_risk='Crítico'
        ).count(),

        'Alto': Patient.objects.filter(
            disease_risk='Alto'
        ).count(),

        'Medio': Patient.objects.filter(
            disease_risk='Medio'
        ).count(),

        'Bajo': Patient.objects.filter(
            disease_risk='Bajo'
        ).count(),
    }

    return Response({

        'total_patients': total_patients,
        'critical_patients': critical_patients,
        'average_glucose': round(average_glucose, 2),
        'average_bmi': round(average_bmi, 2),
        'risk_distribution': risk_distribution

    })


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