from django.urls import path
from . import views

urlpatterns = [
    path('analytics/estadisticas/', views.estadisticas_descriptivas, name='analytics-estadisticas'),
    path('analytics/kpis/',         views.kpis_medicos,              name='analytics-kpis'),
    path('analytics/segmentacion/', views.segmentacion,              name='analytics-segmentacion'),
    path('analytics/criticos/',     views.pacientes_criticos,        name='analytics-criticos'),
]