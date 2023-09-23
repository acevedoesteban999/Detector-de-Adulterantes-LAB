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
    path('list/',ModelListView.as_view(),name='mod_list'),
    path('add/',ModelCreateView.as_view(),name='mod_add'),
    path('data/<int:pk>/',ModelDataView.as_view(),name='mod_data'),
    path('update/<int:pk>/',ModelUpdateView.as_view(),name='mod_update'),
    path('delete/<int:pk>/',ModelDeleteView.as_view(),name='mod_delete'),
]
