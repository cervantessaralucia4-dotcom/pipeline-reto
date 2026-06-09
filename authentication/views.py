# ═══════════════════════════════════════════════════════════════
#  authentication/views.py
#  Endpoints:
#    POST /api/auth/register/  — crear usuario con rol
#    GET  /api/auth/me/        — perfil del usuario autenticado
#    GET  /api/auth/users/     — listar usuarios (solo admin)
#    PUT  /api/auth/users/<id>/rol/ — cambiar rol (solo admin)
# ═══════════════════════════════════════════════════════════════
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema

from .models import UserProfile
from .serializers import RegisterSerializer, UserSerializer, LoginResponseSerializer
from .permissions import IsAdministrador, get_rol


# ── POST /api/auth/register/ ──────────────────────────────────
@extend_schema(
    tags=['Autenticación'],
    summary='Registrar nuevo usuario',
    description='Crea un usuario con rol (administrador, medico, analista). Solo administradores.',
    request=RegisterSerializer,
    responses={201: UserSerializer},
)
@api_view(['POST'])
@permission_classes([IsAdministrador])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ── GET /api/auth/me/ ─────────────────────────────────────────
@extend_schema(
    tags=['Autenticación'],
    summary='Perfil del usuario autenticado',
    description='Retorna los datos del usuario actual incluyendo su rol.',
    responses={200: UserSerializer},
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me_view(request):
    # Crear perfil automáticamente si no tiene (superusuario creado por CLI)
    if not hasattr(request.user, 'profile'):
        UserProfile.objects.get_or_create(
            user=request.user,
            defaults={'rol': 'administrador'}
        )
    return Response(UserSerializer(request.user).data)


# ── GET /api/auth/users/ ──────────────────────────────────────
@extend_schema(
    tags=['Autenticación'],
    summary='Listar todos los usuarios',
    description='Lista todos los usuarios del sistema con sus roles. Solo administradores.',
    responses={200: UserSerializer(many=True)},
)
@api_view(['GET'])
@permission_classes([IsAdministrador])
def users_list(request):
    users = User.objects.select_related('profile').all().order_by('id')
    return Response(UserSerializer(users, many=True).data)


# ── PUT /api/auth/users/<id>/rol/ ─────────────────────────────
@extend_schema(
    tags=['Autenticación'],
    summary='Cambiar rol de un usuario',
    description='Cambia el rol de un usuario. Solo administradores.',
    request={'application/json': {
        'type': 'object',
        'required': ['rol'],
        'properties': {
            'rol': {'type': 'string', 'enum': ['administrador', 'medico', 'analista']}
        }
    }},
    responses={200: UserSerializer},
)
@api_view(['PUT'])
@permission_classes([IsAdministrador])
def change_rol(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({'error': 'Usuario no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    rol = request.data.get('rol')
    if rol not in ('administrador', 'medico', 'analista'):
        return Response(
            {'error': 'Rol inválido. Opciones: administrador, medico, analista.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    profile, _ = UserProfile.objects.get_or_create(user=user)
    profile.rol = rol
    profile.save()

    return Response(UserSerializer(user).data)