from rest_framework import serializers
from .models import Patient


class PatientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Patient
        fields = [
            'id',
            'first_name',
            'last_name',
            'age',
            'sex',
            'weight',
            'height',
            'bmi',
            'systolic_pressure',
            'diastolic_pressure',
            'heart_rate',
            'glucose',
            'cholesterol',
            'oxygen_saturation',
            'temperature',
            'family_history',
            'smoker',
            'alcohol_consumption',
            'physical_activity',
            'preliminary_diagnosis',
            'disease_risk',
            'consultation_date',
        ]
        read_only_fields = ['bmi']