from django import forms
from .models import Model
from core.tra.models import Training
#from core.meas.models import Measuring,MeasuringData
import time
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
        try:
            import numpy as np
            #from sklearn.datasets import load_digits
            import tensorflow as tf
            #from tensorflow.keras import layers
            from tinymlgen import port
            #from tensorflow.keras.models import load_model
            from config.settings import BASE_DIR
            import os
            # m=Model.objects.create(
            #     name=self.cleaned_data.get('name'),
            # )
            # for l in _list:
            #     Training.objects.get(pk=l).models.add(m)
            # d=[]
            # l=[]
            # for t in m.training_model.all():
            #     for measuring in t.measuring_trainig.all():
            #         d.append(measuring.get_list_data()) 
            #         l.append(measuring.get_predict_index())
            #print(d)
            #print(l)
            #_in=np.array(d,dtype=float)
            #_out=np.array(l,dtype=int)
            _in=np.array([1,6,30,7,70,45,503,291,99],dtype=float)
            _out=np.array([0.254,0.1524,0.762,0.1778,1.778,1.0922,12.776,5.1054,2.514],dtype=float)
            model=tf.keras.Sequential()
            model.add(tf.keras.layers.Dense(units=1,input_shape=[1]))
            model.compile(
                optimizer=tf.keras.optimizers.Adam(0.1),
                loss='mean_squared_error',
            )

            train=model.fit(
                _in,
                _out,
                epochs=500,
            )

            model.save(os.path.join(BASE_DIR,f"media/models/_{self.cleaned_data.get('name')}.h5"))
            model.save_weights(os.path.join(BASE_DIR,f"media/models/_w_{self.cleaned_data.get('name')}.h5"))
            
        except:
            pass
        pass
        #import numpy as np
        # from sklearn.model_selection import train_test_split
        # from sklearn.preprocessing import StandardScaler
        # from sklearn.decomposition import PCA
        # from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
        # def get_n_c(x_standar_scaler_train):
        #     pca=PCA().fit(x_standar_scaler_train)
        #     var=pca.explained_variance_ratio_
        #     _d=0
        #     for c,d in enumerate(var,start=1):
        #         _d+=d
        #         if _d>0.95:
        #             return c
        # X=[]
        # y=[]

        # for t in Training.objects.filter(pk__in=_list):
        #     for m in t.measuring_trainig.all():
        #         X.append(m.get_list_data())
        #         y.append(m.get_predict_index()) 
        # print(X)
        # print(y)        
        # X_train, X_test, y_train, y_test = train_test_split(X, y)
        # sclaer = StandardScaler()
        # x_ss_train=sclaer.fit_transform(X_train)
        # n_c=get_n_c(x_ss_train)
        # pca = PCA(n_components=n_c)
        # x_pca_train=pca.fit(x_ss_train)
        # lda=LDA(n_components=n_c)
        # lda.fit(x_pca_train)
        
        # # import numpy as np
        # # import matplotlib.pyplot as plt
        
        # #plt.plot(np.cumsum(var))
        # #plt.show()
        
        # pass    
        # # m=Model.objects.create(
        # #     name=self.cleaned_data.get('name'),
        # #     #file_model=f"{self.cleaned_data.get('name')}.txt"
        # # )
        # # for l in _list:
        # #     Training.objects.get(pk=l).models.add(m)
        # # d=[]
        # # l=[]
        # # for t in m.training_model.all():
        # #     for measuring in t.measuring_trainig.all():
        # #         d.append(measuring.get_list_data()) 
        # #         l.append(measuring.get_predict_index())
        # # print(d)
        # # print(l)
        
        
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
        
    