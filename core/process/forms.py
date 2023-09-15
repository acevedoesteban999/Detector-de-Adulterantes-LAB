from django import forms
from .models import Measuring

class MeasuringForm(forms.ModelForm):
    def initial():
        last=Measuring.objects.order_by('-id').first()
        return last.id + 1 if last else 0     
    
    id=forms.FloatField(required=True,disabled=True,initial=initial(),widget=forms.NumberInput(attrs={'class':'form-control'}))
    class Meta:
        model =Measuring
        fields = 'name','id',
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control','placeholder': 'Ingrese un nombre'}),
        }
    def save(self):
        import time
        time.sleep(5)
        #Measuring.objects.create(
        #    name=self.cleaned_data['name'],
            #chanel
        #)