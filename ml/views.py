from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from authentication.permissions import IsAnalista, IsMedicoOrAnalista
from .models import MLMetrics
from .serializers import MLMetricsSerializer
from .train_model import train_model
from patients.predict import predict_risk


@extend_schema(tags=['Machine Learning'], summary='Entrenar modelo Random Forest',
               description='Entrena el modelo y guarda métricas. Acceso: Analista y Administrador.')
@api_view(['POST'])
@permission_classes([IsAnalista])
def train_view(request):
    try:
        resultado = train_model()
        metricas = MLMetrics.objects.create(
            usuario=request.user,
            accuracy=resultado['accuracy'], precision=resultado['precision'],
            recall=resultado['recall'], f1_score=resultado['f1_score'],
            confusion_matrix=resultado['confusion_matrix'],
            total_registros=resultado['total_registros'],
            registros_train=resultado['registros_train'],
            registros_test=resultado['registros_test'],
            modelo=resultado['modelo'], features=resultado['features'],
            importancia=resultado['importancia'],
        )
        return Response({
            'mensaje': 'Modelo entrenado correctamente.', 'metrics_id': metricas.pk,
            'accuracy': resultado['accuracy'], 'precision': resultado['precision'],
            'recall': resultado['recall'], 'f1_score': resultado['f1_score'],
            'confusion_matrix': resultado['confusion_matrix'],
            'clases': resultado['clases'], 'importancia': resultado['importancia'],
            'total_registros': resultado['total_registros'],
            'registros_train': resultado['registros_train'],
            'registros_test': resultado['registros_test'],
            'reporte': resultado['reporte'],
        })
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(tags=['Machine Learning'], summary='Métricas del último entrenamiento',
               description='Acceso: Médico, Analista y Administrador.')
@api_view(['GET'])
@permission_classes([IsMedicoOrAnalista])
def metrics_view(request):
    ultimo = MLMetrics.objects.first()
    if not ultimo:
        return Response({'error': 'No hay entrenamientos. Ejecuta POST /api/ml/train/ primero.'},
                        status=status.HTTP_404_NOT_FOUND)
    return Response(MLMetricsSerializer(ultimo).data)


@extend_schema(tags=['Machine Learning'], summary='Historial de entrenamientos',
               description='Acceso: Analista y Administrador.')
@api_view(['GET'])
@permission_classes([IsAnalista])
def historial_view(request):
    todos = MLMetrics.objects.all()[:20]
    return Response(MLMetricsSerializer(todos, many=True).data)


@extend_schema(
    tags=['Machine Learning'],
    summary='Predecir riesgo de un paciente',
    description='Acceso: Médico, Analista y Administrador.',
    request={'application/json': {'type': 'object', 'required': ['edad','IMC','glucosa','colesterol','presión_sistólica','frecuencia_cardiaca'],
        'properties': {
            'edad': {'type': 'number', 'example': 55},
            'IMC': {'type': 'number', 'example': 32.1},
            'glucosa': {'type': 'number', 'example': 320.0},
            'colesterol': {'type': 'number', 'example': 240.0},
            'presión_sistólica': {'type': 'number', 'example': 185},
            'frecuencia_cardiaca': {'type': 'number', 'example': 95},
        }}},
)
@api_view(['POST'])
@permission_classes([IsMedicoOrAnalista])
def predict_view(request):
    campos = ['edad','IMC','glucosa','colesterol','presión_sistólica','frecuencia_cardiaca']
    faltantes = [c for c in campos if c not in request.data]
    if faltantes:
        return Response({'error': f'Campos faltantes: {faltantes}'}, status=status.HTTP_400_BAD_REQUEST)
    resultado = predict_risk(request.data)
    if 'error' in resultado:
        return Response(resultado, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(resultado)