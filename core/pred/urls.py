"""
URL configuration for milk_processing project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import *
from django.views.generic import RedirectView
urlpatterns = [
    path('add/',PredictionCreateView.as_view(),name='pred_add'),
    path('add/real_time/',PredictionCreateRealTimeView.as_view(),name='pred_add_real'),
    path('add/data/',PredictionCreateDataView.as_view(),name='pred_add_data'),
    path('update/<int:pk>/',PredictionUpdateView.as_view(),name='pred_update'),
    path('reg/list/',PredictionListView.as_view(),name='pred_list'),
    path('reg/delete/<int:pk>/',PredictionDeleteView.as_view(),name='pred_delete'),
]
