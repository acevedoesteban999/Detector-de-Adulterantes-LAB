from django import forms
from .models import Measuring,MeasuringData,Training
import time
from config.utils import is_at_migrations
from .utils import MeasuringI2C
        
        
class MeasuringForm(forms.ModelForm):
    #def initial():
    #    if not is_at_migrations():
    #        last=Measuring.objects.order_by('-id').first()
    #        return last.id + 1 if last else 0     
    #id=forms.FloatField(required=True,disabled=True,initial=initial(),widget=forms.NumberInput(attrs={'class':'form-control'}))
    class Meta:
        model =Measuring
        fields = 'name',#'id',
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control','placeholder': 'Ingrese un nombre'}),
        }
    def update(self,pk):
        obj=Measuring.objects.get(pk=pk)
        obj.name=self.cleaned_data['name']
        obj.save()
        
    def save(self):
        MeasuringI2C(self.cleaned_data.get('name'))
            