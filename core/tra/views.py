from django.shortcuts import render,redirect
from .models import *
from django.urls import reverse_lazy
from django.views.generic import TemplateView,FormView,ListView,UpdateView,DeleteView,DetailView,View,ArchiveIndexView
from core.log.utils import MyLoginRequiredMixin
from .forms import *
from core.meas.models import Measuring,MeasuringData
from django.contrib import messages
from django.http import HttpResponse,FileResponse
#import pandas as pd
from io import StringIO
import csv
        
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
        multi='Training with this Nombre already exists' in form.errors.as_text()
        if form.is_valid() or multi:
            return self.form_valid(request,form,multi)
        else:
            return self.form_invalid(request,form,"data no válida")
    
    def form_invalid(self,request,form,rason=""):
        messages.error(request,f'Error al crear entrnamiento, {rason}')
        return super().form_invalid(form)
    
    def form_valid(self,request,form,multi):
        form.save(multi)
        messages.success(request,f"{'Creada nuevo' if multi==False else 'Actualizado'} entrenamiento correctamente")
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
        context['training_save_exel']=True
        context['pk']=self.pk
        context['back_url']=reverse_lazy('tra_list')
        return context

class TrainingMultiDataView(MyLoginRequiredMixin,DetailView):
    template_name='data_tra.html'
    model=Training
    def dispatch(self, request, *args, **kwargs):
        self.pk = kwargs['pk']
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Training.objects.get(pk=self.pk).name
        context['objects_meas']=Measuring.objects.filter(training=self.pk)
        context['objects_label']=Measuring.lamdas()
        context['back_url']=reverse_lazy('tra_list')
        return context

class TrainingDownloadCSVDataView(MyLoginRequiredMixin,View):
    
    def get(self,request,*args, **kwargs):
        def newcsv(data, fieldnames):
            """
            Create a new csv file that represents generated data.
            """
            new_csvfile = StringIO()
            wr = csv.writer(new_csvfile, quoting=csv.QUOTE_ALL)
            wr = csv.DictWriter(new_csvfile, fieldnames = fieldnames)
            l=[]
            for _d in data:
                d={}
                for count in range(len(fieldnames)):
                    d.update({fieldnames[count]:_d[count]})
                l.append(d)
            wr.writeheader()
            for _l in l:
                wr.writerow(_l)
            return new_csvfile
        measuring=Training.objects.get(pk=kwargs.get('pk')).measuring_trainig.all()
        l1=[]
        for m in measuring:
            l2=[]
            for md in m.measuring_data.all():
                l2.append(md.value)
            l2.append([PredictionChoices.index(item)+1 for item in PredictionChoices if item[0] == m.predict][0])
            l1.append(l2)
        labels=Measuring.chanels()
        labels.append("label")
        csvfile = newcsv(l1, labels)
        response = HttpResponse(csvfile.getvalue(), content_type='text/csv')
        response['Content-Disposition'] = f"attachment; filename={Training.objects.get(pk=kwargs.get('pk')).name}.csv"
        return response
    
    # def get_pandas(self,request,*args, **kwargs):
        #     measuring=Training.objects.get(pk=kwargs.get('pk')).measuring_trainig.all()
        #     l1=[]
        #     for m in measuring:
        #         l2=[]
        #         for md in m.measuring_data.all():
        #             l2.append(md.value)
        #         l2.append([PredictionChoices.index(item)+1 for item in PredictionChoices if item[0] == m.predict][0])
        #         l1.append(l2)
        #     labels=Measuring.chanels()
        #     labels.append("label")
        #     df = pd.DataFrame( l1 ,columns = labels )
        #     response = HttpResponse(content_type='text/csv')
        #     response['Content-Disposition'] ='attachment; filename=export.csv'  
        #     df.to_csv(path_or_buf=response,index=False)  
        #     return response
        
class TrainingCSVView(MyLoginRequiredMixin,FormView):
    template_name='csv_tra.html'
    success_url=reverse_lazy('tra_list')
    form_class=CSVForm
    def form_valid(self, form) :
        form.save()
        return super().form_valid(form)