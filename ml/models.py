from django.db import models
from django.contrib.auth.models import User


class MLMetrics(models.Model):
    """Guarda las métricas de cada entrenamiento del modelo."""

    fecha_entrenamiento = models.DateTimeField(auto_now_add=True)
    usuario             = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='ml_entrenamientos'
    )

    # Métricas
    accuracy  = models.FloatField()
    precision = models.FloatField()
    recall    = models.FloatField()
    f1_score  = models.FloatField()

    # Matriz de confusión guardada como JSON
    confusion_matrix = models.JSONField()

    # Info del entrenamiento
    total_registros = models.IntegerField(default=0)
    registros_train = models.IntegerField(default=0)
    registros_test  = models.IntegerField(default=0)
    modelo          = models.CharField(max_length=100, default='RandomForestClassifier')
    features        = models.JSONField(default=list)
    importancia     = models.JSONField(default=dict)

    class Meta:
        ordering = ['-fecha_entrenamiento']
        verbose_name        = 'Métricas ML'
        verbose_name_plural = 'Métricas ML'

    def __str__(self):
        return f"ML #{self.pk} — Accuracy: {self.accuracy:.4f} — {self.fecha_entrenamiento:%Y-%m-%d}"