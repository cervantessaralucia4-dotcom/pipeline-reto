from rest_framework import serializers
from .models import Patient


class PatientSerializer(serializers.ModelSerializer):

    nombres = serializers.CharField(source='first_name')
    apellidos = serializers.CharField(source='last_name')
    edad = serializers.IntegerField(source='age')
    sexo = serializers.CharField(source='sex')

    peso = serializers.FloatField(source='weight')
    altura = serializers.FloatField(source='height')
    IMC = serializers.FloatField(source='bmi')

    presión_sistólica = serializers.IntegerField(source='systolic_pressure')
    presión_diastólica = serializers.IntegerField(source='diastolic_pressure')

    frecuencia_cardiaca = serializers.IntegerField(source='heart_rate')

    glucosa = serializers.FloatField(source='glucose')
    colesterol = serializers.FloatField(source='cholesterol')

    saturación_oxígeno = serializers.FloatField(source='oxygen_saturation')

    temperatura = serializers.FloatField(source='temperature')

    antecedentes_familiares = serializers.BooleanField(source='family_history')

    fumador = serializers.BooleanField(source='smoker')

    consumo_alcohol = serializers.BooleanField(source='alcohol_consumption')

    actividad_física = serializers.CharField(source='physical_activity')

    diagnóstico_preliminar = serializers.CharField(
        source='preliminary_diagnosis'
    )

    riesgo_calculado = serializers.CharField(
        source='disease_risk'
    )

    fecha_consulta = serializers.DateField(
        source='consultation_date'
    )

    class Meta:
        model = Patient

        fields = [
            'id',
            'nombres',
            'apellidos',
            'edad',
            'sexo',
            'peso',
            'altura',
            'IMC',
            'presión_sistólica',
            'presión_diastólica',
            'frecuencia_cardiaca',
            'glucosa',
            'colesterol',
            'saturación_oxígeno',
            'temperatura',
            'antecedentes_familiares',
            'fumador',
            'consumo_alcohol',
            'actividad_física',
            'diagnóstico_preliminar',
            'riesgo_calculado',
            'fecha_consulta'
        ]