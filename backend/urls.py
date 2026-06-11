from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT
    path('api/token/',         TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(),    name='token_refresh'),

    # Apps
    path('api/', include('authentication.urls')),
    path('api/', include('patients.urls')),
    path('api/', include('etl.urls')),
    path('api/', include('analytics.urls')),
    path('api/', include('ml.urls')),

    # Swagger
    path('api/schema/',  SpectacularAPIView.as_view(),                        name='schema'),
    path('api/docs/',    SpectacularSwaggerView.as_view(url_name='schema'),   name='swagger-ui'),
    path('api/redoc/',   SpectacularRedocView.as_view(url_name='schema'),     name='redoc'),
]

# ── Servir React (frontend build) en producción ──────────────
_index_path = settings.BASE_DIR / 'frontend' / 'build' / 'index.html'
if _index_path.exists():
    urlpatterns += [
        re_path(r'^$', TemplateView.as_view(template_name='index.html')),
        re_path(r'^(?!api/|admin/).*$', TemplateView.as_view(template_name='index.html')),
    ]
    import os
    _TEMPLATES_DIR = str(settings.BASE_DIR / 'frontend' / 'build')
    settings.TEMPLATES[0]['DIRS'].append(_TEMPLATES_DIR)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)