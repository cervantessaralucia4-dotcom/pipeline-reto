# ═══════════════════════════════════════════════════════════════
#  ml/views.py
#  Endpoints:
#    POST /api/ml/train/      — entrena el modelo y guarda métricas
#    GET  /api/ml/metrics/    — métricas del último entrenamiento
#    GET  /api/ml/historial/  — historial de todos los entrenamientos
#    POST /api/ml/predict/    — predicción individual con probabilidades
# ═══════════════════════════════════════════════════════════════
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import MLMetrics
from .serializers import MLMetricsSerializer
from .train_model import train_model
from patients.predict import predict_risk


# ── POST /api/ml/train/ ───────────────────────────────────────
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def train_view(request):
    """
    Entrena el modelo RandomForest con el dataset limpio,
    guarda las métricas en BD y retorna los resultados.
    """
    try:
        resultado = train_model()

        # Guardar métricas en BD
        metricas = MLMetrics.objects.create(
            usuario          = request.user,
            accuracy         = resultado['accuracy'],
            precision        = resultado['precision'],
            recall           = resultado['recall'],
            f1_score         = resultado['f1_score'],
            confusion_matrix = resultado['confusion_matrix'],
            total_registros  = resultado['total_registros'],
            registros_train  = resultado['registros_train'],
            registros_test   = resultado['registros_test'],
            modelo           = resultado['modelo'],
            features         = resultado['features'],
            importancia      = resultado['importancia'],
        )

        return Response({
            'mensaje':          'Modelo entrenado correctamente.',
            'metrics_id':       metricas.pk,
            'accuracy':         resultado['accuracy'],
            'precision':        resultado['precision'],
            'recall':           resultado['recall'],
            'f1_score':         resultado['f1_score'],
            'confusion_matrix': resultado['confusion_matrix'],
            'clases':           resultado['clases'],
            'importancia':      resultado['importancia'],
            'total_registros':  resultado['total_registros'],
            'registros_train':  resultado['registros_train'],
            'registros_test':   resultado['registros_test'],
            'reporte':          resultado['reporte'],
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ── GET /api/ml/metrics/ ──────────────────────────────────────
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def metrics_view(request):
    """Retorna las métricas del último entrenamiento."""
    ultimo = MLMetrics.objects.first()
    if not ultimo:
        return Response(
            {'error': 'No hay entrenamientos registrados. Ejecuta POST /api/ml/train/ primero.'},
            status=status.HTTP_404_NOT_FOUND
        )
    serializer = MLMetricsSerializer(ultimo)
    return Response(serializer.data)


# ── GET /api/ml/historial/ ────────────────────────────────────
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def historial_view(request):
    """Lista el historial de todos los entrenamientos."""
    todos = MLMetrics.objects.all()[:20]
    serializer = MLMetricsSerializer(todos, many=True)
    return Response(serializer.data)


# ── POST /api/ml/predict/ ─────────────────────────────────────
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def predict_view(request):
    """
    Predice el riesgo de un paciente individual.
    Body esperado:
    {
        "edad": 45,
        "IMC": 27.5,
        "glucosa": 130.0,
        "colesterol": 210.0,
        "presión_sistólica": 145,
        "frecuencia_cardiaca": 88
    }
    """
    campos = ['edad', 'IMC', 'glucosa', 'colesterol',
              'presión_sistólica', 'frecuencia_cardiaca']

    faltantes = [c for c in campos if c not in request.data]
    if faltantes:
        return Response(
            {'error': f'Campos faltantes: {faltantes}'},
            status=status.HTTP_400_BAD_REQUEST
        )

    resultado = predict_risk(request.data)

    if 'error' in resultado:
        return Response(resultado, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(resultado, status=status.HTTP_200_OK)