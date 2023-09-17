from typing import Any, Dict
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView,FormView,ListView,UpdateView,DeleteView
from core.log.utils import MyLoginRequiredMixin
from .forms import MeasuringForm
from .models import Measuring,MeasuringData
from django.contrib import messages
# Create your views here.

class MainView(MyLoginRequiredMixin,TemplateView):
    template_name='process.html'
    
class MeasuringListView(MyLoginRequiredMixin,ListView):
    template_name='list_meas.html'
    model=Measuring

class MeasuringCreateView(MyLoginRequiredMixin,FormView):
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
        return redirect('meas_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Nueva Medición"
        return context

class MeasuringUpdateView(MyLoginRequiredMixin,UpdateView):
    model=Measuring
    template_name = '_form.html'
    form_class=MeasuringForm
    #permission_required="user.change_user"
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            #form=self.get_form()
            form.update(kwargs.get('pk'))
            messages.success(self.request,'Actualizado correctamente')
        else:
            messages.error(request,'Error al Actualizar')

        return redirect('meas_list')
        
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Actualizar Información"
        context['url_cancel']=reverse_lazy('meas_list')
        return context

class MeasuringDeleteView(MyLoginRequiredMixin,DeleteView):
    model=Measuring
    template_name = 'delete_meas.html'
    #permission_required="user.delete_user"
    success_url=reverse_lazy('meas_list')
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Eliminar Muestra"
        context['url_cancel']=reverse_lazy('meas_list')   
        context['name']=self.object.name
        return context


class MeasuringDataView(MyLoginRequiredMixin,ListView):
    template_name='meas_data.html'
    model=MeasuringData
    def dispatch(self, request, *args, **kwargs):
        self.pk = kwargs['pk']
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Measuring.objects.get(pk=self.pk).name
        
        context['back_url']=reverse_lazy('meas_list')
        return context
    
    
    
class ChartsView(MyLoginRequiredMixin,TemplateView):
    template_name='process.html'
    
class TrainView(MyLoginRequiredMixin,TemplateView):
    template_name='process.html'
    
        