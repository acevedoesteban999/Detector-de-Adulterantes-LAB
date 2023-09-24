from django.shortcuts import render,redirect,HttpResponse
from .models import *
from django.urls import reverse_lazy
from django.views.generic import TemplateView,FormView,ListView,UpdateView,DeleteView,DetailView
from core.log.utils import MyLoginRequiredMixin
from .forms import *
from core.meas.models import Measuring,MeasuringData
from core.tra.models import Training
from django.contrib import messages
from django.db.models import Q
# Create your views here.
class ModelListView(MyLoginRequiredMixin,ListView):
    paginate_by=10
    template_name='list_mod.html'
    model=Model    
    def get_queryset(self):
        return super().get_queryset().order_by('-datetime')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Modelos"
        context['back_url']=reverse_lazy('reg')
        return context
    
class ModelCreateView(MyLoginRequiredMixin,FormView):
    template_name='add_mod.html'
    form_class=ModelForm
    
    def post(self, request, *args, **kwargs):
        print(request.POST)
        if self.is_ajax():
            if request.POST.get('action')=="search_trining":
                search=request.POST.get('data')
                if not search:
                    return HttpResponse("")
                #q=(Q(name__contains=search_value) | Q(id__contains=search_value))
                trainings=Training.objects.filter(name__contains=search)[:5]
                return render(request,'sea_tra.html',context={'trainings':trainings,'search':search})
                            
        self._list=[int(x) for x in request.POST.get('list_pk').split(',')] 
        
        form = self.get_form()
        
        if form.is_valid():
            return self.form_valid(request,form)
        else:
            return self.form_invalid(request,form,"data no válida")
    
    def form_invalid(self,request,form,rason=""):
        messages.error(request,f'Error al crear modelo, {rason}')
        return super().form_invalid(form)
    
    def form_valid(self,request,form):
        try:
            form.save(self._list)
        except Exception as e:
            return self.form_invalid(request,form,e)
        messages.success(request,'Creada nuevo modelo correctamente')
        return redirect('tra_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Nuevo Modelo"
        return context
       
class ModelUpdateView(MyLoginRequiredMixin,UpdateView):
    model=Training
    template_name = '_form.html'
    form_class=ModelUpdateForm
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
        context['url_cancel']=reverse_lazy('mod_list')
        return context

class ModelDeleteView(MyLoginRequiredMixin,DeleteView):
    model=Model
    template_name = 'delete_meas.html'
    #permission_required="user.delete_user"
    success_url=reverse_lazy('meas_list')
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Eliminar Entrenamiento"
        context['url_cancel']=reverse_lazy('tra_list')   
        context['name']=self.object.name
        return context

class ModelDataView(MyLoginRequiredMixin,ListView):
    template_name='list_tra.html'
    model=Training
    def dispatch(self, request, *args, **kwargs):
        self.pk = kwargs['pk']
        return super().dispatch(request, *args, **kwargs)
    def get_queryset(self):
        print(Training.objects.filter(models=self.pk))
        print(Training.objects.all().values())
        return super().get_queryset().filter(models__id=self.pk)
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Training.objects.get(pk=self.pk).name
        
        context['back_url']=reverse_lazy('mod_list')
        return context

