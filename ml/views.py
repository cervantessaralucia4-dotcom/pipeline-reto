from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import MLMetrics
from .serializers import MLMetricsSerializer
from .train_model import train_model
from patients.predict import predict_risk


@extend_schema(
    tags=['Machine Learning'],
    summary='Entrenar modelo Random Forest',
    description=(
        'Entrena el modelo de clasificación de riesgo con el dataset limpio actual. '
        'Guarda el modelo como .pkl y registra las métricas en la base de datos. '
        'Variables predictoras: edad, IMC, glucosa, colesterol, presión sistólica, frecuencia cardíaca.'
    ),
    responses={200: MLMetricsSerializer},
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def train_view(request):
    try:
        resultado = train_model()
        metricas = MLMetrics.objects.create(
            usuario         = request.user,
            accuracy        = resultado['accuracy'],
            precision       = resultado['precision'],
            recall          = resultado['recall'],
            f1_score        = resultado['f1_score'],
            confusion_matrix= resultado['confusion_matrix'],
            total_registros = resultado['total_registros'],
            registros_train = resultado['registros_train'],
            registros_test  = resultado['registros_test'],
            modelo          = resultado['modelo'],
            features        = resultado['features'],
            importancia     = resultado['importancia'],
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
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(
    tags=['Machine Learning'],
    summary='Métricas del último entrenamiento',
    description='Retorna accuracy, precision, recall, F1 y matriz de confusión del último modelo entrenado.',
    responses={200: MLMetricsSerializer},
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def metrics_view(request):
    ultimo = MLMetrics.objects.first()
    if not ultimo:
        return Response(
            {'error': 'No hay entrenamientos. Ejecuta POST /api/ml/train/ primero.'},
            status=status.HTTP_404_NOT_FOUND
        )
    return Response(MLMetricsSerializer(ultimo).data)


@extend_schema(
    tags=['Machine Learning'],
    summary='Historial de entrenamientos',
    description='Lista los últimos 20 entrenamientos del modelo con sus métricas.',
    responses={200: MLMetricsSerializer(many=True)},
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def historial_view(request):
    todos = MLMetrics.objects.all()[:20]
    return Response(MLMetricsSerializer(todos, many=True).data)


@extend_schema(
    tags=['Machine Learning'],
    summary='Predecir riesgo de un paciente',
    description=(
        'Recibe los datos clínicos de un paciente y retorna el nivel de riesgo predicho '
        'junto con la probabilidad de cada clase (Bajo, Medio, Alto, Crítico).'
    ),
    request={
        'application/json': {
            'type': 'object',
            'required': ['edad','IMC','glucosa','colesterol','presión_sistólica','frecuencia_cardiaca'],
            'properties': {
                'edad':                 {'type': 'number', 'example': 55},
                'IMC':                  {'type': 'number', 'example': 32.1},
                'glucosa':              {'type': 'number', 'example': 320.0},
                'colesterol':           {'type': 'number', 'example': 240.0},
                'presión_sistólica':    {'type': 'number', 'example': 185},
                'frecuencia_cardiaca':  {'type': 'number', 'example': 95},
            }
        }
    },
    responses={200: {'type': 'object', 'properties': {
        'riesgo_predicho': {'type': 'string', 'example': 'Crítico'},
        'probabilidades':  {'type': 'object'},
    }}},
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def predict_view(request):
    campos = ['edad','IMC','glucosa','colesterol','presión_sistólica','frecuencia_cardiaca']
    faltantes = [c for c in campos if c not in request.data]
    if faltantes:
        return Response({'error': f'Campos faltantes: {faltantes}'}, status=status.HTTP_400_BAD_REQUEST)

    resultado = predict_risk(request.data)
    if 'error' in resultado:
        return Response(resultado, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(resultado, status=status.HTTP_200_OK)