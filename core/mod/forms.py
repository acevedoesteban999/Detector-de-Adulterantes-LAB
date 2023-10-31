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

class ModelLoadForm(forms.Form):
    zip_model=forms.FileField(label="ZIP",widget=forms.FileInput(attrs={'class':'form-control'}))
    def save(self):
        import io
        import zipfile
        
        zip=self.cleaned_data['zip_model']
        _name=str(zip).replace(".zip","")
        contenido_zip = io.BytesIO(zip.read())
        with zipfile.ZipFile(contenido_zip, 'r') as zip_ref:
            
            
            #archivos = zip_ref.namelist()
            model_c=zip_ref.read(_name)
            model_keras=zip_ref.read(_name+".keras")
            model_keras_w=zip_ref.read(_name+"_W.keras")
            m=Model.objects.create(
                name=_name,
                state=False,
            )
            import os
            from config.settings import BASE_DIR
            with open(os.path.join(BASE_DIR,f"media/models/{_name}"),'wb') as file:
                file.write(model_c)
            with open(os.path.join(BASE_DIR,f"media/models/{_name}.keras"),'wb') as file:
                file.write(model_keras)
            with open(os.path.join(BASE_DIR,f"media/models/{_name}_W.keras"),'wb') as file:
                file.write(model_keras_w)
            m.state=True
            m.save()
            return _name        
            
   
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
        
    