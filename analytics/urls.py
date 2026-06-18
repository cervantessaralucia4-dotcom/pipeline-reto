from django.urls import path
from . import views

urlpatterns = [
    path('analytics/estadisticas/', views.estadisticas_descriptivas, name='analytics-estadisticas'),
    path('analytics/kpis/',         views.kpis_medicos,              name='analytics-kpis'),
    path('analytics/segmentacion/', views.segmentacion,              name='analytics-segmentacion'),
    path('analytics/criticos/',     views.pacientes_criticos,        name='analytics-criticos'),
    path('analytics/pacientes-por-filtro/', views.pacientes_por_filtro, name='analytics-pacientes-filtro'),
    path('analytics/export/csv/',  views.export_filtro_csv,  name='analytics-export-filtro-csv'),
    path('analytics/export/pdf/',  views.export_filtro_pdf,  name='analytics-export-filtro-pdf'),
]