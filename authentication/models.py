# ═══════════════════════════════════════════════════════════════
#  authentication/models.py
#  Extiende el User de Django con un perfil que incluye el rol.
#  Roles: administrador, medico, analista
# ═══════════════════════════════════════════════════════════════
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):

    ROLES = [
        ('administrador', 'Administrador'),
        ('medico',        'Médico'),
        ('analista',      'Analista'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    rol = models.CharField(
        max_length=20,
        choices=ROLES,
        default='medico'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = 'Perfil de usuario'
        verbose_name_plural = 'Perfiles de usuarios'

    def __str__(self):
        return f"{self.user.username} — {self.get_rol_display()}"