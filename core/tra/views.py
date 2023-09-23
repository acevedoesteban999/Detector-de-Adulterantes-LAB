from django.shortcuts import render,redirect
from .models import *
from django.urls import reverse_lazy
from django.views.generic import TemplateView,FormView,ListView,UpdateView,DeleteView,DetailView
from core.log.utils import MyLoginRequiredMixin
from .forms import *
from core.meas.models import Measuring,MeasuringData
from django.contrib import messages
# Create your views here.

class TrainingListView(MyLoginRequiredMixin,ListView):
    paginate_by=10
    template_name='list_tra.html'
    model=Training    
    def get_queryset(self):
        return super().get_queryset().order_by('-datetime')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Entrenamientos"
        context['back_url']=reverse_lazy('reg')
        return context
    
class TrainingCreateView(MyLoginRequiredMixin,FormView):
    template_name='add_tra.html'
    form_class=TrainingingForm
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        
        if form.is_valid():
            return self.form_valid(request,form)
        else:
            return self.form_invalid(request,form,"data no válida")
    
    def form_invalid(self,request,form,rason=""):
        messages.error(request,f'Error al crear entrnamiento, {rason}')
        return super().form_invalid(form)
    
    def form_valid(self,request,form):
        try:
            form.save()
        except Exception as e:
            return self.form_invalid(request,form,e)
        messages.success(request,'Creada nuevo entrenamiento correctamente')
        return redirect('tra_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Nuevo entrenamiento"
        return context
       
class TrainingUpdateView(MyLoginRequiredMixin,UpdateView):
    model=Training
    template_name = '_form.html'
    form_class=TrainingingUpdateForm
    #permission_required="user.change_user"
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.update(kwargs.get('pk'))
            messages.success(self.request,'Actualizado correctamente')
        else:
            messages.error(request,'Error al Actualizar')

        return redirect('tra_list')
        
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Actualizar Información"
        context['url_cancel']=reverse_lazy('tra_list')
        return context

class TrainingDeleteView(MyLoginRequiredMixin,DeleteView):
    model=Training
    template_name = 'delete_meas.html'
    #permission_required="user.delete_user"
    success_url=reverse_lazy('meas_list')
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Eliminar Entrenamiento"
        context['url_cancel']=reverse_lazy('tra_list')   
        context['name']=self.object.name
        return context

class TrainingDataView(MyLoginRequiredMixin,ListView):
    template_name='list_meas.html'
    model=Measuring
    def dispatch(self, request, *args, **kwargs):
        self.pk = kwargs['pk']
        return super().dispatch(request, *args, **kwargs)
    def get_queryset(self):
        return super().get_queryset().filter(training=self.pk)
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Training.objects.get(pk=self.pk).name
        
        context['back_url']=reverse_lazy('reg')
        return context

