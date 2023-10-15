from django import forms
from .models import Training
from core.meas.models import Measuring,MeasuringData
import time
from config.utils import thread_is_alive
from .utils import train_thread
from threading import Thread
from core.meas.models import PredictionChoices

try:
    import pandas as pd
    W=True
except:
    W=False
import csv
class TrainingingForm(forms.ModelForm):
    prediction = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}),choices=PredictionChoices,)
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
        global W
        if W==True:
            return self.save_pandas()
        if self.cleaned_data.get('_1f')==True:
            return self.save1()
        _count=self.cleaned_data.get('count')
        _r=self.cleaned_data.get('csv').read().decode("utf-8").splitlines()[1:_count]
        rows=[]
        for r in _r:
           rows.append(r.split(',')) 
        t=Training.objects.create(
            name=self.cleaned_data.get('name'),
            predict="C",
            )
        for count in range(len(rows)):
            prediction=PredictionChoices[int(rows[count][18])-1][0]
            
            m=Measuring.objects.create(
                name=f"T~{self.cleaned_data.get('name')}~{count}",
                training=t,
                predict=prediction
            )
            t.count+=1
            for c,d in enumerate(rows[count]):
                if c==18:
                    break
                MeasuringData.objects.create(
                    chanel= Measuring.chanels()[c],
                    value=float(d),
                    measuring=m
                )
        t.save() 
    def save1(self):
        _count=self.cleaned_data.get('count')
        _r=self.cleaned_data.get('csv').read().decode("utf-8").splitlines()[1:_count]
        rows=[]
        for r in _r:
           rows.append(r.split(',')) 
        t=Training.objects.create(
            name=self.cleaned_data.get('name'),
            predict="C",
            )
        for count in range(len(rows)):
            
            prediction=PredictionChoices[int(rows[count][1])-1][0]
            
            m=Measuring.objects.create(
                name=f"T~{self.cleaned_data.get('name')}~{count}",
                training=t,
                predict=prediction
            )
            t.count+=1
            for c,d in enumerate(rows[count],start=-2):
                if c<0:
                    continue
                MeasuringData.objects.create(
                    chanel= Measuring.chanels()[c],
                    value=float(d),
                    measuring=m
                )
        t.save() 
    def save_pandas(self):
        if self.cleaned_data.get('_1f')==True:
            return self.save1_pandas()
        _count=self.cleaned_data.get('count')
        csv=pd.read_csv(self.cleaned_data.get('csv'))[0:_count]
        t=Training.objects.create(
            name=self.cleaned_data.get('name'),
            predict="C",
            )
        for count in range(csv.shape[0]):
            prediction=PredictionChoices[csv.iloc[count,18]-1][0]    
            m=Measuring.objects.create(
                name=f"T~{self.cleaned_data.get('name')}~{count}",
                training=t,
                predict=prediction
            )
            t.count+=1
            for c,d in enumerate(csv.iloc[count]):
                if c==18:
                    break
                MeasuringData.objects.create(
                    chanel= Measuring.chanels()[c],
                    value=d,
                    measuring=m
                )
        t.save()  
    def save1_pandas(self):
        _count=self.cleaned_data.get('count')
        csv=pd.read_csv(self.cleaned_data.get('csv'))[0:_count]
        t=Training.objects.create(
            name=self.cleaned_data.get('name'),
            predict="C",
            )
        for count in range(csv.shape[0]):
            prediction=PredictionChoices[csv.iloc[count,1]][0]
            m=Measuring.objects.create(
                name=f"T~{self.cleaned_data.get('name')}~{count}",
                training=t,
                predict=prediction
            )
            t.count+=1
            for c,d in enumerate(csv.iloc[count],start=-2):
                if c<0:
                    continue
                MeasuringData.objects.create(
                    chanel= Measuring.chanels()[c],
                    value=d,
                    measuring=m
                )
        t.save() 