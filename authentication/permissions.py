# ═══════════════════════════════════════════════════════════════
#  authentication/permissions.py
#  Permisos personalizados por rol.
#
#  Roles y accesos:
#  ┌───────────────┬────────────────────────────────────────────┐
#  │ Administrador │ Acceso total a todos los módulos           │
#  │ Médico        │ Solo lectura: pacientes, dashboard         │
#  │ Analista      │ ETL, analytics, ML, lectura de pacientes   │
#  └───────────────┴────────────────────────────────────────────┘
# ═══════════════════════════════════════════════════════════════
from rest_framework.permissions import BasePermission


def get_rol(user):
    """Retorna el rol del usuario o None si no tiene perfil."""
    try:
        return user.profile.rol
    except Exception:
        return None


class IsAdministrador(BasePermission):
    """Solo administradores."""
    message = 'Acceso restringido: se requiere rol Administrador.'

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            (get_rol(request.user) == 'administrador' or request.user.is_superuser)
        )


class IsMedico(BasePermission):
    """Solo médicos (y administradores)."""
    message = 'Acceso restringido: se requiere rol Médico o Administrador.'

    def has_permission(self, request, view):
        rol = get_rol(request.user)
        return bool(
            request.user and
            request.user.is_authenticated and
            (rol in ('medico', 'administrador') or request.user.is_superuser)
        )


class IsAnalista(BasePermission):
    """Solo analistas (y administradores)."""
    message = 'Acceso restringido: se requiere rol Analista o Administrador.'

    def has_permission(self, request, view):
        rol = get_rol(request.user)
        return bool(
            request.user and
            request.user.is_authenticated and
            (rol in ('analista', 'administrador') or request.user.is_superuser)
        )


class IsMedicoOrAnalista(BasePermission):
    """Médicos, analistas y administradores."""
    message = 'Acceso restringido: se requiere rol Médico, Analista o Administrador.'

    def has_permission(self, request, view):
        rol = get_rol(request.user)
        return bool(
            request.user and
            request.user.is_authenticated and
            (rol in ('medico', 'analista', 'administrador') or request.user.is_superuser)
        )