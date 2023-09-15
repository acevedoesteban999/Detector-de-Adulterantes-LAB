from django.shortcuts import render,redirect
from django.views.generic import TemplateView,FormView
from core.log.utils import MyLoginRequiredMixin
from .forms import MeasuringForm
from .models import Measuring
from django.contrib import messages
# Create your views here.


class MainView(MyLoginRequiredMixin,TemplateView):
    template_name='process.html'
    
class MeasuringView(MyLoginRequiredMixin,FormView):
    template_name='measuring.html'
    form_class=MeasuringForm
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        
        if form.is_valid():
            return self.form_valid(request,form)
        else:
            return self.form_invalid(request)
    
    def form_invalid(self,request,form):
        messages.error(request,'Error al crear medición')
        return super().form_invalid(form)
    
    def form_valid(self,request,*args, **kwargs):
        form=args[0]
        form.save()
        messages.success(request,'Creada nueva medición correctamente')
        return redirect('main')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Nueva Medición"
        return context


class RegistersView(MyLoginRequiredMixin,TemplateView):
    template_name='process.html'
    
class ChartsView(MyLoginRequiredMixin,TemplateView):
    template_name='process.html'
    
class TrainView(MyLoginRequiredMixin,TemplateView):
    template_name='process.html'
    
        