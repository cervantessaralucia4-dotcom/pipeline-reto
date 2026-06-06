from django.contrib import admin
from .models import MLMetrics

@admin.register(MLMetrics)
class MLMetricsAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'usuario', 'fecha_entrenamiento',
        'accuracy', 'precision', 'recall', 'f1_score', 'modelo'
    ]
    list_filter  = ['modelo', 'fecha_entrenamiento']
    readonly_fields = [
        'accuracy', 'precision', 'recall', 'f1_score',
        'confusion_matrix', 'importancia', 'features',
        'total_registros', 'registros_train', 'registros_test',
    ]