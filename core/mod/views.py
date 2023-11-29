from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse
from django.core import serializers
from .models import *
from django.urls import reverse_lazy
from django.views.generic import TemplateView,FormView,ListView,UpdateView,DeleteView,DetailView,View
from core.log.utils import MyLoginRequiredMixin
from .forms import *
from config.utils import thread_is_alive
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
        objs=Model.objects.filter(state=None)
        if objs.count()!=0:
            if not thread_is_alive("ThreadModel"):
              for o in objs:
                  o.state=False
                  o.save()  
        
        return super().get_queryset().order_by('-datetime')
    
    def post(self, request, *args, **kwargs):
        if self.is_ajax():
            if request.POST.get('action')=="thread_finish":
                th_al=thread_is_alive("ThreadModel")
                return HttpResponse(th_al)
            
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Modelos"
        context['back_url']=reverse_lazy('reg')
        context['thread_alive']=thread_is_alive("ThreadModel")
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
                objects=Training.objects.filter(name__contains=search,state=True)[:5]
                return render(request,'sea_tra.html',context={'objects':objects,'search':search})
        try:                    
            self._list=[int(x) for x in request.POST.get('list_pk').split(',')] 
        except:
            self._list=[]
        form = self.get_form()
        
        if form.is_valid():
            return self.form_valid(request,form)
        else:
            return self.form_invalid(request,form,"Data no válida")
    
    def form_invalid(self,request,form,rason=""):
        messages.error(request,f'Error al crear modelo, {rason}')
        BinnacleMessages.warning("Error",rason)
        return super().form_invalid(form)
    
    def form_valid(self,request,form):
        try:
            optim_model=None
            if request.user.has_perm('is_development'):
                optim_model=request.POST.get("optim_model")
            if not(form.save(self._list,optim_model)):
                return self.form_invalid(request,form,rason="Ya se está entrenando un modelo")
        except Exception as e:
            return self.form_invalid(request,form,e)
        messages.success(request,f"Se ha iniciado el proceso de creación de entrenamiento del modelo {form.cleaned_data['name']}")
        return redirect('mod_list')
    
    def get_context_data(self, **kwargs):
        # from matplotlib import pyplot as plt
        # from sklearn.metrics import confusion_matrix
        # from config.settings import MEDIA_ROOT
        # import seaborn as sns
        # import matplotlib
        # matplotlib.use('Agg')
        # plt.clf()
        # y_test=[0,1,2,1,2]
        # y=[0,0,2,0,2]
        # cm=confusion_matrix(y_test,y)
        # sns.heatmap(cm, annot=True, cmap='Blues', fmt='d', cbar=False)
        # plt.xlabel('Etiquetas Predichas')
        # plt.ylabel('Etiquetas Reales')
        # plt.title('Matriz de Confusión')
        # plt.tight_layout()
        # plt.savefig(MEDIA_ROOT+"/trains/"+f"name_confusion_matrix_all.png")
        context = super().get_context_data()
        context['title'] = "Nuevo Modelo"
        return context
       
class ModelUpdateView(MyLoginRequiredMixin,UpdateView):
    model=Model
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
    success_url=reverse_lazy('mod_list')
    def form_valid(self, form):
        name=self.get_object().name
        os.remove(
            MEDIA_ROOT+"/models/"+f"{name}.keras",
        )
        os.remove(
            MEDIA_ROOT+"/models/"+f"{name}_W.keras",
        )
        os.remove(
            MEDIA_ROOT+"/models/"+f"{name}",
        )
        os.remove(
            MEDIA_ROOT+"/trains/"+f"{name}_accuracy.png",
        )
        os.remove(
            MEDIA_ROOT+"/trains/"+f"{name}_loss.png",
        )
        os.remove(
            MEDIA_ROOT+"/trains/"+f"{name}_confusion_matrix.png",
        )
        return super().form_valid(form)
    # def delete(self, request, *args, **kwargs):
    #     print("DELET")
    #     print(kwargs)
    #     raise Exception()
    #     os.remove(
    #         MEDIA_ROOT+"/models/"+f"{last_nme}.keras",
    #     )
    #     os.remove(
    #         MEDIA_ROOT+"/models/"+f"{last_nme}_W.keras",
    #     )
    #     os.remove(
    #         MEDIA_ROOT+"/models/"+f"{last_nme}",
    #     )
    #     os.remove(
    #         MEDIA_ROOT+"/trains/"+f"{last_nme}_accuracy.png",
    #     )
    #     os.remove(
    #         MEDIA_ROOT+"/trains/"+f"{last_nme}_loss.png",
    #     )
    #     os.remove(
    #         MEDIA_ROOT+"/trains/"+f"{last_nme}_confusion_matrix.png",
    #     )
    #     return super().delete(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Eliminar Entrenamiento"
        context['url_cancel']=reverse_lazy('mod_list')   
        context['name']=self.object.name
        return context

class ModelDataView(MyLoginRequiredMixin,ListView):
    template_name='list_tra_mod.html'
    model=Training
    def dispatch(self, request, *args, **kwargs):
        self.pk = kwargs['pk']
        return super().dispatch(request, *args, **kwargs)
    def get_queryset(self):
        objs=Training.objects.filter(state=None)
        if objs.count()!=0:
            if not thread_is_alive("ThreadTrainings"):
              for o in objs:
                  o.state=False
                  o.save()  
        return super().get_queryset().filter(models__id=self.pk)
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        m=Model.objects.get(pk=self.pk)
        context['title'] = m.name
        context['back_url']=reverse_lazy('mod_list')
        return context

class ModelLoadView(MyLoginRequiredMixin,FormView):
    template_name='_form.html'
    form_class=ModelLoadForm
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(request,form)
        else:
            return self.form_invalid(request,form,"Data no válida")
    
    def form_invalid(self,request,form,rason=""):
        messages.error(request,f'Error al cargar modelo, {rason}')
        return super().form_invalid(form)
    
    def form_valid(self,request,form):
        name=form.save()
        messages.success(request,f"Se ha cargado el modelo {name}")
        return redirect('mod_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Nuevo Modelo"
        return context

class ModelUploadView(MyLoginRequiredMixin,View):
    
    def get(self,request,*args, **kwargs):
        from git import Repo,Git
        from django.http import HttpResponse, Http404   
        import os
        from config.settings import BASE_DIR,MEDIA_ROOT
        import shutil
        # Crear un objeto de archivo ZIP en memoria
        pk=kwargs.get('pk')
        _name=Model.objects.get(pk=pk).name.replace(" ","_")
        try:
            r=Repo("../files/")
            r.git.checkout("tesis")
            r.remote().pull()
            shutil.copy2(os.path.join(BASE_DIR,f"media/models/{_name}"),BASE_DIR.__str__().replace("Tesis","files"))
            r.index.add([f"{_name}"])
            r.index.commit(f"AutoCommit: {_name}")
            r.remote().push()
            return render(request,"html_upload.html",context={"MSG":f"Se ha actualizado correctamente el modelo {_name}","URL":f"https://raw.githubusercontent.com/Esteban1914/files/tesis/{_name}"})
        except Exception as e:
            print(e)
            return render(request,"html_upload.html",context={"MSG":f"Error al actualizar modelo {_name}","Error":e})

class ModelDownloadView(MyLoginRequiredMixin,View):
    
    def get(self,request,*args, **kwargs):
        from django.http import HttpResponse, Http404        
        import os
        from config.settings import MEDIA_ROOT
        import io
        import zipfile

        try:
            zip_data = io.BytesIO()
            pk=kwargs.get('pk')
            _name=Model.objects.get(pk=pk).name.replace(" ","_")
            with zipfile.ZipFile(zip_data, 'w') as archive:
                archive.write(arcname=f"{_name}",filename= os.path.join(MEDIA_ROOT, f"models/{_name}"))  
                archive.write(arcname=f"{_name}.keras",filename= os.path.join(MEDIA_ROOT, f"models/{_name}.keras"))  
                archive.write(arcname=f"{_name}_W.keras",filename= os.path.join(MEDIA_ROOT, f"models/{_name}_W.keras")) 

            zip_data.seek(0)
            response = HttpResponse(zip_data.read(), content_type="application/zip")
            response['Content-Disposition'] = 'attachment; filename=' + _name + ".zip"
            return response
        except Exception as e:
            print(e)
            raise Http404
