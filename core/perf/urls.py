from django.urls import path
from .views import PerformanceView

urlpatterns = [
    path('',PerformanceView.as_view(),name='perf'),
]
