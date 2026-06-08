from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    # Admin Django
    path('admin/', admin.site.urls),

    # ── JWT ──────────────────────────────────────────────────
    path('api/token/',         TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(),    name='token_refresh'),

    # ── Apps ─────────────────────────────────────────────────
    path('api/', include('patients.urls')),
    path('api/', include('etl.urls')),
    path('api/', include('analytics.urls')),
    path('api/', include('ml.urls')),

    # ── Swagger / OpenAPI ────────────────────────────────────
    # Schema JSON/YAML (para herramientas externas)
    path('api/schema/',  SpectacularAPIView.as_view(), name='schema'),
    # Swagger UI interactivo
    path('api/docs/',    SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # ReDoc (alternativa más limpia)
    path('api/redoc/',   SpectacularRedocView.as_view(url_name='schema'),   name='redoc'),
]