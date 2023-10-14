from django import forms
from .models import Model
from core.tra.models import Training
#from core.meas.models import Measuring,MeasuringData
import time
from threading import Thread
from config.utils import thread_is_alive
from .utils import trin_model_thread
#from config.utils import is_at_migrations
class ModelForm(forms.ModelForm):
    trainings = forms.CharField(widget=forms.Textarea(),label="Entrenamientos",required=False,disabled=True)
    search=forms.CharField(label='Buscar Entrenamientos',max_length=20, required=False,widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'Buscar Entrenamiento'}),)
    class Meta:
        model =Model
        fields = 'name','trainings','search',
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control','placeholder': 'Ingrese un nombre'}),
        }
    def save(self,_list):
        if not thread_is_alive("ThreadModel"):
            Thread(target=trin_model_thread,name="ThreadModel",args=(self.cleaned_data.get('name'),_list,)).start()
            return True
        return False
        
class ModelUpdateForm(forms.ModelForm):
    class Meta:
        model =Model
        fields = 'name',
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control','placeholder': 'Ingrese un nombre'}),
        }
    def update(self,pk):
        obj=Model.objects.get(pk=pk)
        obj.name=self.cleaned_data['name']
        obj.save()
        
    