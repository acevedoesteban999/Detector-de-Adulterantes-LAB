from django import forms
from .models import Measuring,MeasuringData,Training
from .as7265x import AS7265X
import time
from config.utils import is_at_migrations

def getData(name,training=None):
    try:
        from smbus import SMBus    
        _as7265x=AS7265X(SMBus(1))
        _as7265x.begin()
        _as7265x.takeMeasurementsWithBulb()
        _l=['A','B','C','D','E','F','G','H','I','J','K','L','R','S','T','U','V','W']
        measuring=Measuring.objects.create(
            name=name,
            training=training,
        )
        for l in _l:
            MeasuringData.objects.create(
                chanel=l,
                value=eval(f"_as7265x.getCalibrated{l}()"),
                measuring=measuring,
            )
    except ModuleNotFoundError:
        import random
        _l=['A','B','C','D','E','F','G','H','I','J','K','L','R','S','T','U','V','W']
        
        measuring=Measuring.objects.create(
            name=name,
            training=training,
        )
        for l in _l:
            print(l)
            MeasuringData.objects.create(
                chanel=l,
                value=random.randint(0,10000/100),
                measuring=measuring,
            )
def getTrainData(name,count):
    tr=Training.objects.create(
        name=name,
        count=count,
    )
    for count in range(int(count)):
        get1Data(f"TR~{tr.name}~{count}",tr)
        time.sleep(2)
class TrainingingForm(forms.ModelForm):
    class Meta:
        model =Training
        fields = 'name','count',
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control','placeholder': 'Ingrese un nombre'}),
            'count': forms.TextInput(attrs={'class':'form-control','placeholder': 'Ingrese cantidad de muestras'}),
        }
    def update(self,pk):
        obj=Training.objects.get(pk=pk)
        obj.name=self.cleaned_data['name']
        obj.save()
        
    def save(self):
        getTrainData(self.cleaned_data.get('name'),self.cleaned_data.get('count'))
        
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
        getData(self.cleaned_data.get('name'))
        # try:
        #     from smbus import SMBus    
        #     _as7265x=AS7265X(SMBus(1))
        #     _as7265x.begin()
        #     _as7265x.takeMeasurementsWithBulb()
        #     _l=['A','B','C','D','E','F','G','H','I','J','K','L','R','S','T','U','V','W']
        #     measuring=Measuring.objects.create(
        #         name=self.cleaned_data['name'],
        #     )
        #     for l in _l:
        #         MeasuringData.objects.create(
        #             chanel=l,
        #             value=eval(f"_as7265x.getCalibrated{l}()"),
        #             measuring=measuring,
        #         )
        # except ModuleNotFoundError:
        #     import random
        #     _l=['A','B','C','D','E','F','G','H','I','J','K','L','R','S','T','U','V','W']
        #     measuring=Measuring.objects.create(
        #         name=self.cleaned_data['name'],
        #     )
        #     for l in _l:
        #         MeasuringData.objects.create(
        #             chanel=l,
        #             value=random.randint(0,10000/100),
        #             measuring=measuring,
        #         )
            