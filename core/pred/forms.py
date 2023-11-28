from django import forms
from .models import Prediction
from core.mod.models import Model
from core.meas.models import Measuring
from config.utils import PredictionChoices
import time
#from config.utils import is_at_migrations
from core.meas.utils import MeasuringI2C
import os
from config.settings import BASE_DIR
from .utils import prediction_thread,prediction_thread1
from threading import Thread
from config.utils import thread_is_alive

class PredictionForm(forms.ModelForm):
    #models = forms.CharField(widget=forms.Textarea(),label="Modelos",required=False,disabled=True)
    #search=forms.CharField(label='Buscar Modelos',max_length=20, required=False,widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'Buscar Modelo'}),)
    
    class Meta:
        model =Prediction
        fields= 'name',#'models','search',
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control','placeholder': 'Ingrese un nombre'}),
          }
    
    
    def update(self,pk):
        obj=Prediction.objects.get(pk=pk)
        obj.name=self.cleaned_data['name']
        obj.save()
        
    def save(self,_model_pk):
        if not thread_is_alive("ThreadPrediction"):
            Thread(target=prediction_thread,name="ThreadPrediction",args=(self.cleaned_data.get('name'),_model_pk,)).start()
            return True
        return False
    def save1(self,_model_pk,_train_pk):
        if not thread_is_alive("ThreadPrediction"):
            Thread(target=prediction_thread1,name="ThreadPrediction",args=(self.cleaned_data.get('name'),_model_pk,_train_pk,)).start()
            return True
        return False
        