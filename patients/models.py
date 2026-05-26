from django.db import models


class Patient(models.Model):

    SEX_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]

    RISK_CHOICES = [
        ('Bajo', 'Bajo'),
        ('Medio', 'Medio'),
        ('Alto', 'Alto'),
        ('Crítico', 'Crítico'),
    ]

    ACTIVITY_CHOICES = [
        ('Baja', 'Baja'),
        ('Media', 'Media'),
        ('Alta', 'Alta'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    age = models.IntegerField()

    sex = models.CharField(
        max_length=1,
        choices=SEX_CHOICES
    )

    weight = models.FloatField()
    height = models.FloatField()

    bmi = models.FloatField(blank=True, null=True)

    systolic_pressure = models.IntegerField()
    diastolic_pressure = models.IntegerField()

    heart_rate = models.IntegerField()

    glucose = models.FloatField()
    cholesterol = models.FloatField()

    oxygen_saturation = models.FloatField()

    temperature = models.FloatField()

    family_history = models.BooleanField(default=False)

    smoker = models.BooleanField(default=False)

    alcohol_consumption = models.BooleanField(default=False)

    physical_activity = models.CharField(
        max_length=20,
        choices=ACTIVITY_CHOICES
    )

    preliminary_diagnosis = models.CharField(max_length=255)

    disease_risk = models.CharField(
        max_length=20,
        choices=RISK_CHOICES
    )

    consultation_date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_bmi(self):
        return round(self.weight / (self.height ** 2), 2)

    def save(self, *args, **kwargs):
        self.bmi = self.calculate_bmi()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"