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
    path('reg/list/',TrainingListView.as_view(),name='tra_list'),
    path('add/',TrainingCreateView.as_view(),name='tra_add'),
    path('reg/data/<int:pk>/',TrainingDataView.as_view(),name='tra_data'),
    path('reg/update/<int:pk>/',TrainingUpdateView.as_view(),name='tra_update'),
    path('reg/delete/<int:pk>/',TrainingDeleteView.as_view(),name='tra_delete'),
    path('csv/',TrainingCSVView.as_view(),name='tra_csv'),
    path('reg/multidata/<int:pk>/',TrainingMultiDataView.as_view(),name='tra_multidata'),
     path('downlaod_csv/<int:pk>/',TrainingDownloadCSVDataView.as_view(),name='tra_downl_csv'),
]
