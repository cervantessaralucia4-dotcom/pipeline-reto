from django.urls import path
from . import views

urlpatterns = [
    path('ml/train/',    views.train_view,    name='ml-train'),
    path('ml/metrics/',  views.metrics_view,  name='ml-metrics'),
    path('ml/historial/', views.historial_view, name='ml-historial'),
    path('ml/predict/',  views.predict_view,  name='ml-predict'),
]