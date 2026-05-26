import pandas as pd

from django.core.management.base import BaseCommand

from patients.models import Patient


class Command(BaseCommand):

    help = 'Carga pacientes desde CSV limpio'

    def handle(self, *args, **kwargs):

        file_path = 'datasets/clean_clinical_dataset.csv'

        df = pd.read_csv(file_path)

        created = 0

        for _, row in df.iterrows():

            Patient.objects.create(

                first_name=row['nombres'],
                last_name=row['apellidos'],
                age=int(row['edad']),
                sex='M' if row['sexo'] == 'Masculino' else 'F',

                weight=row['peso'],
                height=row['altura'],

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

                physical_activity='Media',

                preliminary_diagnosis=row[
                    'diagnóstico_preliminar'
                ],

                disease_risk=row[
                    'riesgo_calculado'
                ],

                consultation_date=row[
                    'fecha_consulta'
                ]
            )

            created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'\nPacientes cargados: {created}'
            )
        )