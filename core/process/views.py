from typing import Any, Dict
from django.shortcuts import render,redirect
from django.views.generic import TemplateView,FormView,ListView
from core.log.utils import MyLoginRequiredMixin
from .forms import MeasuringForm
from .models import Measuring
from django.contrib import messages
# Create your views here.
class Ina():
    def __init__(self):
        self.i=0
    def inc_i(self):
        self.i=self.i+1
    def get_i(self):
        return self.i
ina=Ina()
class MainView(MyLoginRequiredMixin,TemplateView):
    template_name='processs.html'
    def get_context_data(self, **kwargs):
        global ina
        context = super().get_context_data(**kwargs)
        context["i"] = ina.get_i()
        ina.inc_i()   
        return context
    


class MeasuringView(MyLoginRequiredMixin,FormView):
    template_name='measuring.html'
    form_class=MeasuringForm
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        
        if form.is_valid():
            return self.form_valid(request,form)
        else:
            return self.form_invalid(request,form,"data no válida")
    
    def form_invalid(self,request,form,rason=""):
        messages.error(request,f'Error al crear medición, {rason}')
        return super().form_invalid(form)
    
    def form_valid(self,request,form):
        try:
            form.save()
        except Exception as e:
            return self.form_invalid(request,form,e)
        messages.success(request,'Creada nueva medición correctamente')
        return redirect('reg')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Nueva Medición"
        return context


class RegistersView(MyLoginRequiredMixin,ListView):
    template_name='registers.html'
    model=Measuring
    
    
    
class ChartsView(MyLoginRequiredMixin,TemplateView):
    template_name='process.html'
    
class TrainView(MyLoginRequiredMixin,TemplateView):
    template_name='process.html'
    
        