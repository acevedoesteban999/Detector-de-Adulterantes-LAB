from django.shortcuts import render
from django.views.generic import TemplateView
from core.log.utils import MyLoginRequiredMixin
from django.http import JsonResponse  
import random
# Create your views here.


class ProcessView(MyLoginRequiredMixin,TemplateView):
    template_name='process.html'
    def post(self,request):
        if self.is_ajax():
            if request.POST.get('action')=="data":
                return JsonResponse({'response':random.randint(0,25)},safe=False)
        return None
        