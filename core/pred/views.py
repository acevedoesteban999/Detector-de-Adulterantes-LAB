from typing import Any, Dict
from django.shortcuts import render,redirect,HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView,FormView,ListView,UpdateView,DeleteView,DetailView
from core.log.utils import MyLoginRequiredMixin
from core.mod.models import Model
from core.tra.models import Training
from .forms import *
from .models import Prediction
from core.binn.models import BinnacleMessages
from django.contrib import messages
# Create your views here.

class PredictionCreateView(MyLoginRequiredMixin,TemplateView):
    template_name="pred.html"

class PredictionCreateDataView(MyLoginRequiredMixin,FormView):
    template_name='add_pred_data.html'
    form_class=PredictionForm
    #permission_required="is_"
    def post(self, request, *args, **kwargs):
        if self.is_ajax():
            if request.POST.get('action')=="search_models":
                search=request.POST.get('data')
                if not search:
                    return HttpResponse("")
                objects=Model.objects.filter(name__contains=search,state=True)[:5]
                return render(request,'sea_mod.html',context={'objects':objects,'search':search})
            elif request.POST.get('action')=="search_trainin":
                search=request.POST.get('data')
                if not search:
                    return HttpResponse("")
                objects=Training.objects.filter(name__contains=search,state=True)[:5]
                return render(request,'sea_mod.html',context={'objects':objects,'search':search,"pref":"1"})
        form = self.get_form()
        try:                    
            self._model_pk=int(request.POST.get('list_pk'))
            self._train_pk=int(request.POST.get('list_pk_data'))
        except:
            self._list=None
        if form.is_valid():
            return self.form_valid(request,form)
        else:
            return self.form_invalid(request,form,"Data no válida")
    
    def form_invalid(self,request,form,rason=""):
        messages.error(request,f'Error al crear predicción, {rason}')
        BinnacleMessages.warning("Error",rason)
        return super().form_invalid(form)
    
    def form_valid(self,request,form):
        try:
            if not form.save1(self._model_pk,self._train_pk):
                return self.form_invalid(request,form,rason="Ya se está prediciendo")
        except Exception as e:
            return self.form_invalid(request,form,e)
        messages.success(request,'Creada nueva predicción correctamente')
        return redirect('pred_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Nueva Predicción"
        return context

class PredictionCreateRealTimeView(MyLoginRequiredMixin,FormView):
    template_name='add_pred_real_time.html'
    form_class=PredictionForm
    #permission_required="is_"
    def post(self, request, *args, **kwargs):
        if self.is_ajax():
            if request.POST.get('action')=="search_models":
                search=request.POST.get('data')
                if not search:
                    return HttpResponse("")
                #q=(Q(name__contains=search_value) | Q(id__contains=search_value))
                objects=Model.objects.filter(name__contains=search,state=True)[:5]
                return render(request,'sea_mod.html',context={'objects':objects,'search':search})
        form = self.get_form()
        try:                    
            self._model_pk=int(request.POST.get('list_pk'))
        except:
            self._list=None
        if form.is_valid():
            return self.form_valid(request,form)
        else:
            return self.form_invalid(request,form,"Data no válida")
    
    def form_invalid(self,request,form,rason=""):
        messages.error(request,f'Error al crear predicción, {rason}')
        BinnacleMessages.warning("Error",rason)
        return super().form_invalid(form)
    
    def form_valid(self,request,form):
        try:
            if not form.save(self._model_pk):
                return self.form_invalid(request,form,rason="Ya se está prediciendo")
        except Exception as e:
            return self.form_invalid(request,form,e)
        messages.success(request,'Creada nueva predicción correctamente')
        return redirect('pred_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Nueva Predicción"
        return context

class PredictionListView(MyLoginRequiredMixin,ListView):
    paginate_by = 10
    template_name='list_pred.html'
    model=Prediction
    
    def get_queryset(self):
        objs=Prediction.objects.filter(state=None)
        if objs.count()!=0:
            if not thread_is_alive("ThreadPrediction"):
                for o in objs:
                  o.state=False
                  o.save()  
        return super().get_queryset().order_by('-datetime')
    
    def post(self, request, *args, **kwargs):
        if self.is_ajax():
            if request.POST.get('action')=="thread_finish":
                th_al=thread_is_alive("ThreadPrediction")
                return HttpResponse(th_al)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url']=reverse_lazy('reg') 
        context['thread_alive']=thread_is_alive("ThreadPrediction")
        
        return context
    
class PredictionUpdateView(MyLoginRequiredMixin,UpdateView):
    model=Prediction
    template_name = '_form.html'
    form_class=PredictionForm
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.update(kwargs.get('pk'))
            messages.success(self.request,'Actualizado correctamente')
        else:
            messages.error(request,'Error al Actualizar')

        return redirect('pred_list')
        
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Actualizar Información"
        context['url_cancel']=reverse_lazy('pred_list')
        return context

class PredictionDeleteView(MyLoginRequiredMixin,DeleteView):
    model=Prediction
    template_name = 'delete_pred.html'
    #permission_required="user.delete_user"
    success_url=reverse_lazy('pred_list')
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Eliminar Prediccion"
        context['url_cancel']=reverse_lazy('pred_list')   
        context['name']=self.object.name
        return context

