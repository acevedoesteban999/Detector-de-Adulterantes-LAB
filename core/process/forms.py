from django import forms
from .models import Measuring,MeasuringData
from .as7265x import AS7265X
from config.utils import is_at_migrations
class MeasuringForm(forms.ModelForm):
    def initial():
        if not is_at_migrations():
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
        _as7265x=AS7265X()
        _as7265x.begin()
        _as7265x.takeMeasurementsWithBulb()
        _l=['A','B','C','D','E','F','G','H','I','J','K','L','R','S','T','U','V','W']
        measuring=Measuring.objects.create(
            name=self.cleaned_data['name'],
        )
        for l in _l:
            MeasuringData.objects.create(
                chanel=l,
                value=eval(f"_as7265x.getCalibrated{l}()"),
                measuring=measuring,
            )
            