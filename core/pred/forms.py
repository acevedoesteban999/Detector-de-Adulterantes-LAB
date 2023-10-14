from django import forms
from .models import Prediction
from core.meas.models import Measuring
import time
#from config.utils import is_at_migrations
from core.meas.utils import MeasuringI2C
        
        
class PredictionForm(forms.ModelForm):
    class Meta:
        model =Prediction
        fields= 'name',
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control','placeholder': 'Ingrese un nombre'}),
        }
    
    
    def update(self,pk):
        obj=Prediction.objects.get(pk=pk)
        obj.measuring.name=self.cleaned_data['name']
        obj.save()
        
    def save(self):
        print("AA")
        measuring=MeasuringI2C(self.cleaned_data.get('name'))
        p=Prediction(measuring_ptr=measuring)
        p.predict="N"
        p.save_base(raw=True)            