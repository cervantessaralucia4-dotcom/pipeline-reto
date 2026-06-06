from rest_framework import serializers
from .models import MLMetrics


class MLMetricsSerializer(serializers.ModelSerializer):
    usuario = serializers.StringRelatedField()

    class Meta:
        model = MLMetrics
        fields = [
            'id', 'usuario', 'fecha_entrenamiento',
            'accuracy', 'precision', 'recall', 'f1_score',
            'confusion_matrix', 'total_registros',
            'registros_train', 'registros_test',
            'modelo', 'features', 'importancia',
        ]