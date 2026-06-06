from django.db import models
from django.contrib.auth.models import User


class ETLLog(models.Model):

    STATUS_CHOICES = [
        ('exitoso',    'Exitoso'),
        ('fallido',    'Fallido'),
        ('en_proceso', 'En proceso'),
    ]

    usuario = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='etl_logs'
    )

    fecha_inicio     = models.DateTimeField(auto_now_add=True)
    fecha_fin        = models.DateTimeField(null=True, blank=True)
    tiempo_ejecucion = models.FloatField(null=True, blank=True)

    registros_extraidos   = models.IntegerField(default=0)
    registros_duplicados  = models.IntegerField(default=0)
    registros_nulos       = models.IntegerField(default=0)
    registros_fuera_rango = models.IntegerField(default=0)
    registros_cargados    = models.IntegerField(default=0)

    estado         = models.CharField(max_length=20, choices=STATUS_CHOICES, default='en_proceso')
    mensaje        = models.TextField(blank=True)
    archivo_fuente = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name        = 'Log ETL'
        verbose_name_plural = 'Logs ETL'

    def __str__(self):
        return f"ETL #{self.pk} — {self.estado} — {self.fecha_inicio:%Y-%m-%d %H:%M}"