from django.shortcuts import render
from core.log.utils import MyLoginRequiredMixin
from django.views.generic import ListView
from .models import BinnacleMessages
# Create your views here.

class BinnacleView(MyLoginRequiredMixin,ListView):
    template_name="binn.html"
    model=BinnacleMessages
    
    def get_context_data(self, **kwargs) :
        context=super().get_context_data(**kwargs)
        context['title']="Bitácora de Errores"
        context['i_count']=BinnacleMessages.objects.filter(identifier='I').count()
        context['r_count']=BinnacleMessages.objects.filter(identifier='R').count()
        context['a_count']=BinnacleMessages.objects.filter(identifier='A').count()
        context['e_count']=BinnacleMessages.objects.filter(identifier='E').count()
        return context