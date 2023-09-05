from django.shortcuts import render
from django.urls import reverse_lazy
from core.log.utils import MyLoginRequiredMixin
from django.views.generic import TemplateView
from django.http import JsonResponse  
from .utils import *
# Create your views here.

class PerformanceView(MyLoginRequiredMixin,TemplateView):
    template_name="perf.html"
    permission_required="user.view_performance"
    def post(self,request):
        if self.is_ajax():
            if request.POST.get('action')=="cpu":
                return JsonResponse({'response':get_cpu()},safe=False)
            elif request.POST.get('action')=="ram":
                return JsonResponse({'response':get_ram()},safe=False)
            elif request.POST.get('action')=="ethernet":
                return JsonResponse({'response':get_eth()},safe=False)
            elif request.POST.get('action')=="temp":
                return JsonResponse({'response':get_temp()},safe=False)
            elif request.POST.get('action')=="storage":
                return JsonResponse({'response':get_storage()},safe=False)
        return None
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['url']=reverse_lazy('perf')
        return context

