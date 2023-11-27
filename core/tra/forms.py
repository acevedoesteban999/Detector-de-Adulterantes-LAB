from django import forms
from .models import Training
from core.meas.models import Measuring,MeasuringData
import time
from config.utils import thread_is_alive
from .utils import train_thread,csv_thread
from threading import Thread
from core.meas.models import PredictionChoices
import pandas as pd

class TrainingingForm(forms.ModelForm):
    prediction = forms.ChoiceField(label="Predicción",widget=forms.Select(attrs={'class':'form-control'}),choices=PredictionChoices,)
    class Meta:
        model =Training
        fields = 'name','count',
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control','placeholder': 'Ingrese un nombre'}),
            'count': forms.TextInput(attrs={'class':'form-control','placeholder': 'Ingrese cantidad de muestras'}),
        }
        
    def save(self,multi=False):
        if multi==False:
            name=self.cleaned_data.get('name')
        else:
            name=self.data.get('name')
        if not thread_is_alive("ThreadTrainings"):
            Thread(target=train_thread,name="ThreadTrainings",args=(name,self.cleaned_data.get('count'),self.cleaned_data.get('prediction'),)).start()
            return True
        return False
        #TrainingI2C(name,self.cleaned_data.get('count'),self.cleaned_data.get('prediction'))
        
class TrainingingUpdateForm(forms.ModelForm):
    class Meta:
        model =Training
        fields = 'name',
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control','placeholder': 'Ingrese un nombre'}),
        }
    def update(self,pk):
        obj=Training.objects.get(pk=pk)
        obj.name=self.cleaned_data['name']
        obj.save()
        
    
class CSVForm(forms.Form):
    name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'Ingrese un nombre'}))
    csv=forms.FileField(label="CSV",widget=forms.FileInput(attrs={'class':'form-control'}))
    count=forms.IntegerField(required=False,label="Cantidad",widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'Ingrese cantidad datos a cargar '}))
    _1f=forms.BooleanField(required=False,widget=forms.CheckboxInput(),label="Primer Formato")
    def save(self):
        csv_thread(self.cleaned_data.get('_1f'),self.cleaned_data.get('count'),self.cleaned_data.get('csv').read(),self.cleaned_data.get('name'))
        # if not thread_is_alive("ThreadLoadCSV"):
        #     Thread(target=csv_thread,name="ThreadLoadCSV",args=(self.cleaned_data.get('_1f'),self.cleaned_data.get('count'),self.cleaned_data.get('csv').read(),self.cleaned_data.get('name'),)).start()
        #     return True
        return True
        