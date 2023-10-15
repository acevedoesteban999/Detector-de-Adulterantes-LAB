from django import forms
from .models import Prediction
from core.mod.models import Model
from core.meas.models import Measuring
from config.utils import PredictionChoices
import time
#from config.utils import is_at_migrations
from core.meas.utils import MeasuringI2C
from tensorflow import keras
import os
import numpy as np
from config.settings import BASE_DIR

        
class PredictionForm(forms.ModelForm):
    models = forms.CharField(widget=forms.Textarea(),label="Modelos",required=False,disabled=True)
    search=forms.CharField(label='Buscar Modelos',max_length=20, required=False,widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'Buscar Modelo'}),)
    
    class Meta:
        model =Prediction
        fields= 'name','models','search',
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control','placeholder': 'Ingrese un nombre'}),
          }
    
    
    def update(self,pk):
        obj=Prediction.objects.get(pk=pk)
        obj.measuring.name=self.cleaned_data['name']
        obj.save()
        
    def save(self,_model_pk):
        measuring=MeasuringI2C(self.cleaned_data.get('name'))
        model: keras.Sequential= keras.models.load_model(os.path.join(BASE_DIR,f"media/models/_{Model.objects.get(pk=_model_pk).name}.h5"))
        model.load_weights(os.path.join(BASE_DIR,f"media/models/_{Model.objects.get(pk=_model_pk).name}_W.h5"))
        predict_class=model.predict(np.array(measuring.get_list_data(),dtype=float).reshape(1,18)).argmax(axis=-1).tolist()[0]
        print(predict_class)
        p=Prediction(measuring_ptr=measuring)
        p.save_base(raw=True)            
        measuring.predict=PredictionChoices[predict_class][0]
        measuring.save()