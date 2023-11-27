from django.shortcuts import render
from core.log.utils import MyLoginRequiredMixin
from django.views.generic import ListView
from core.binn.models import BinnacleMessages
# Create your views here.

class BinnacleView(MyLoginRequiredMixin,ListView):
    template_name="binn.html"
    model=BinnacleMessages
    permission_required='is_development'
    paginate_by=10
    
    def dispatch(self, request, *args, **kwargs):
        self.kwargs['iden']=kwargs.get('iden')
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        iden:str=self.kwargs.get('iden')    
        if iden in ["I","R","A","E"] :
            return super().get_queryset().filter(identifier=iden).order_by("-timedate")
        return super().get_queryset().order_by("-timedate")
    
    def get_context_data(self, **kwargs) :
        context=super().get_context_data(**kwargs)
        iden:str=self.kwargs.get('iden')
        if iden in ["I","R","A","E"] :
            #context['object_list']=BinnacleMessages.objects.filter(identifier=iden)
            context['iden']=iden
        context['title']="Bitácora de Errores"
        context['i_count']=BinnacleMessages.objects.filter(identifier='I').count()
        context['r_count']=BinnacleMessages.objects.filter(identifier='R').count()
        context['a_count']=BinnacleMessages.objects.filter(identifier='A').count()
        context['e_count']=BinnacleMessages.objects.filter(identifier='E').count()
        return context
    
