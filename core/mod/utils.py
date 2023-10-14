from core.mod.models import Model
def trin_model_thread(name,_list):
        try:
            import time
            m=Model.objects.create(
                name=name,
            )
            import numpy as np
            #from sklearn.datasets import load_digits
            import tensorflow as tf
            #from tensorflow.keras import layers
            from tinymlgen import port
            #from tensorflow.keras.models import load_model
            from config.settings import BASE_DIR
            import os
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
            t=time.time()
            train=model.fit(
                _in,
                _out,
                epochs=500,
            )
            print("T:",time.time()-t)
            model.save(os.path.join(BASE_DIR,f"media/models/_{name}.h5"))
            model.save_weights(os.path.join(BASE_DIR,f"media/models/_{name}_W.h5"))
            m.state=True
        except Exception as e:
            print("Error:",e)
            m.state=False
            
        m.save()
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