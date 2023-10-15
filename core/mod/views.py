from django.shortcuts import render,redirect,HttpResponse
from .models import *
from django.urls import reverse_lazy
from django.views.generic import TemplateView,FormView,ListView,UpdateView,DeleteView,DetailView,View
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
        if self.is_ajax():
            if request.POST.get('action')=="search_trining":
                search=request.POST.get('data')
                if not search:
                    return HttpResponse("")
                #q=(Q(name__contains=search_value) | Q(id__contains=search_value))
                objects=Training.objects.filter(name__contains=search)[:5]
                return render(request,'sea_tra.html',context={'objects':objects,'search':search})
        try:                    
            self._list=[int(x) for x in request.POST.get('list_pk').split(',')] 
        except:
            self._list=[]
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
            if not(form.save(self._list)):
                return self.form_invalid(request,form,rason="Ya se está entrenando un modelo")
        except Exception as e:
            return self.form_invalid(request,form,e)
        messages.success(request,f"Se ha iniciado el proceso de creación de entrenamiento del modelo {form.cleaned_data['name']}")
        return redirect('mod_list')
    
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

        return redirect('mod_list')
        
    
    
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
        context['url_cancel']=reverse_lazy('mod_list')   
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

class ModelDownloadView(MyLoginRequiredMixin,View):
    
    def get(self,request,*args, **kwargs):
        from django.http import HttpResponse, Http404        
        import os
        from config.settings import MEDIA_ROOT
        import io
        import zipfile

        # Crear un objeto de archivo ZIP en memoria
        try:
            zip_data = io.BytesIO()
            pk=kwargs.get('pk')
            _name=Model.objects.get(pk=pk).name.replace(" ","_")
            with zipfile.ZipFile(zip_data, 'w') as archive:
                archive.write(arcname=f"_{_name}.h",filename= os.path.join(MEDIA_ROOT, f"models/_{_name}.h"))  
                archive.write(arcname=f"_{_name}.h5",filename= os.path.join(MEDIA_ROOT, f"models/_{_name}.h5"))  
                archive.write(arcname=f"_{_name}_W.h5",filename= os.path.join(MEDIA_ROOT, f"models/_{_name}_W.h5")) 

            zip_data.seek(0)
            response = HttpResponse(zip_data.read(), content_type="application/zip")
            response['Content-Disposition'] = 'attachment; filename=' + _name + ".zip"
            return response
        except Exception as e:
            print(e)
            raise Http404
