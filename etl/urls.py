from django.urls import path
from . import views

urlpatterns = [
    path('etl/run/',          views.run_etl_view,  name='etl-run'),
    path('etl/historial/',    views.etl_historial, name='etl-historial'),
    path('etl/historial/<int:pk>/', views.etl_detalle, name='etl-detalle'),
]