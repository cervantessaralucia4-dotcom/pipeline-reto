# ═══════════════════════════════════════════════════════════════
#  authentication/serializers.py
# ═══════════════════════════════════════════════════════════════
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model  = UserProfile
        fields = ['rol', 'created_at']


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    rol     = serializers.CharField(write_only=True, required=False, default='medico')

    class Meta:
        model  = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name',
                  'is_active', 'date_joined', 'profile', 'rol']
        read_only_fields = ['id', 'date_joined']


class RegisterSerializer(serializers.ModelSerializer):
    password  = serializers.CharField(write_only=True, min_length=6)
    password2 = serializers.CharField(write_only=True, label='Confirmar contraseña')
    rol       = serializers.ChoiceField(
        choices=['administrador', 'medico', 'analista'],
        default='medico'
    )

    class Meta:
        model  = User
        fields = ['username', 'email', 'first_name', 'last_name',
                  'password', 'password2', 'rol']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password': 'Las contraseñas no coinciden.'})
        return data

    def create(self, validated_data):
        rol = validated_data.pop('rol', 'medico')
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user, rol=rol)
        return user


class LoginResponseSerializer(serializers.Serializer):
    access   = serializers.CharField()
    refresh  = serializers.CharField()
    username = serializers.CharField()
    rol      = serializers.CharField()
    email    = serializers.CharField()