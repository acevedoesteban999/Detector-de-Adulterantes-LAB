from django import forms
from .models import Model
from threading import Thread
from config.utils import thread_is_alive
from .utils import trin_model_thread

class ModelForm(forms.ModelForm):
    neurons=forms.IntegerField(initial=448,min_value=1,max_value=1024,label="Neuronas",widget=forms.NumberInput(attrs={'class':'form-control','placeholder': 'Cantidad de neuronas'}))
    epochs=forms.IntegerField(initial=500,min_value=1,max_value=9999,label="Épocas",widget=forms.NumberInput(attrs={'class':'form-control','placeholder': 'Cantidad de épocas'}))
    class Meta:
        model =Model
        fields = 'name','neurons','epochs','activation',
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control','placeholder': 'Ingrese un nombre'}),
            'activation':forms.Select(attrs={'class':'form-control'}),
        }
    def save(self,_list,optim_model):
        if not thread_is_alive("ThreadModel"):
            Thread(target=trin_model_thread,name="ThreadModel",args=(self.cleaned_data.get('name'),_list,optim_model,self.cleaned_data.get('neurons'),self.cleaned_data.get('epochs'),self.cleaned_data.get('activation'))).start()
            return True
        return False

class ModelLoadForm(forms.Form):
    name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'Ingrese un nombre'}))
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
                name=self.cleaned_data['name'],
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
        
    