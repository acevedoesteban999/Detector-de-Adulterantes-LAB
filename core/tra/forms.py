from django import forms
from .models import Training
#from core.meas.models import Measuring,MeasuringData
import time
#from config.utils import is_at_migrations
from .utils import TrainingI2C
class TrainingingForm(forms.ModelForm):
    class Meta:
        model =Training
        fields = 'name','count',
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control','placeholder': 'Ingrese un nombre'}),
            'count': forms.TextInput(attrs={'class':'form-control','placeholder': 'Ingrese cantidad de muestras'}),
        }
        
    def save(self):
        TrainingI2C(self.cleaned_data.get('name'),self.cleaned_data.get('count'))
        
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
        
    