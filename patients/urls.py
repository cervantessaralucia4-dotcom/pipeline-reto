from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, predict_view, dashboard_kpis, dashboard_charts, reports_view, export_csv_view

router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='patients')

urlpatterns = [
    path('', include(router.urls)),
    path('predict/',          predict_view,     name='predict'),
    path('dashboard/kpis/',   dashboard_kpis,   name='dashboard-kpis'),
    path('dashboard/charts/', dashboard_charts, name='dashboard-charts'),
    path('reportes/',         reports_view,     name='reportes'),
    path('patients/export/csv/', export_csv_view, name='export-csv'),
]