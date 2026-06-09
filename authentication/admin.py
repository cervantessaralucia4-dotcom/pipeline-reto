from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    model  = UserProfile
    can_delete = False
    verbose_name_plural = 'Perfil y Rol'
    fields = ['rol']


class UserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline]
    list_display = ['username', 'email', 'first_name', 'last_name', 'get_rol', 'is_active']

    def get_rol(self, obj):
        try:
            return obj.profile.get_rol_display()
        except Exception:
            return '—'
    get_rol.short_description = 'Rol'


# Re-registrar User con el nuevo admin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(UserProfile)