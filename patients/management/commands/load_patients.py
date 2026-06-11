import pandas as pd

from django.core.management.base import BaseCommand

from patients.models import Patient


class Command(BaseCommand):

    help = 'Carga pacientes desde CSV limpio'

    def handle(self, *args, **kwargs):

        file_path = 'datasets/clean_clinical_dataset.csv'

        df = pd.read_csv(file_path)

        # Limpiar base de datos antes de cargar para evitar duplicados
        self.stdout.write("Limpiando registros existentes de pacientes...")
        Patient.objects.all().delete()

        created = 0
        pacientes = []

        for _, row in df.iterrows():

            pacientes.append(Patient(
                first_name=row['nombres'],
                last_name=row['apellidos'],
                age=int(row['edad']),
                sex=row['sexo'],

                weight=row['peso'],
                height=row['altura'],
                bmi=row['IMC'],

                systolic_pressure=int(row['presión_sistólica']),
                diastolic_pressure=int(row['presión_diastólica']),

                heart_rate=int(row['frecuencia_cardiaca']),

                glucose=row['glucosa'],
                cholesterol=row['colesterol'],

                oxygen_saturation=row['saturación_oxígeno'],

                temperature=row['temperatura'],

                family_history=row['antecedentes_familiares'],

                smoker=row['fumador'],

                alcohol_consumption=row['consumo_alcohol'],

                physical_activity=row['actividad_física'],

                preliminary_diagnosis=row[
                    'diagnóstico_preliminar'
                ],

                disease_risk=row[
                    'riesgo_calculado'
                ],

                consultation_date=row[
                    'fecha_consulta'
                ]
            ))

            created += 1

        Patient.objects.bulk_create(pacientes, ignore_conflicts=True)

        self.stdout.write(
            self.style.SUCCESS(
                f'\nPacientes cargados: {created}'
            )
        )