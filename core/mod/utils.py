from core.mod.models import Model
from core.tra.models import Training
from config.settings import BASE_DIR
import os
import numpy as np
#import tensorflow as tf
from tensorflow import keras
from tinymlgen import port
def trin_model_thread(name,_list):
        try:
            import time
            m=Model.objects.create(
                name=name,
            )
            for l in _list:
                Training.objects.get(pk=l).models.add(m)
            d=[]
            l=[]
            for t in m.training_model.all():
                for measuring in t.measuring_trainig.all():
                    d.append(measuring.get_list_data()) 
                    l.append(measuring.get_predict_index())
            # print(d)
            # print(l)
            _in=np.array(d,dtype=float)
            _out=np.array(l,dtype=int)
            #_in=np.array([1,6,30,7,70,45,503,291,99],dtype=float)
            #_out=np.array([0.254,0.1524,0.762,0.1778,1.778,1.0922,12.776,5.1054,2.514],dtype=float)

            input = keras.Input(shape=(18))
            x = keras.layers.Dense(64, activation="relu")(input)
            output = keras.layers.Dense(5)(x)
            model=keras.Model(input, output)
            #model.add(keras.layers.Input(shape=(18,)))
            #model.add(keras.layers.Dense(64,activation='relu',input_shape=[18]))
            #model.add(keras.layers.Dense(5))
            
            model.compile(
                optimizer=keras.optimizers.Adam(0.1),
                loss='mean_squared_error',
            )
            t=time.time()
            train=model.fit(
                _in,
                _out,
                epochs=500,
            )
            model.save(os.path.join(BASE_DIR,f"media/models/_{name}.h5"))
            model.save_weights(os.path.join(BASE_DIR,f"media/models/_{name}_W.h5"))
            c_code = port(model, variable_name='digits_model', pretty_print=True)
            with open(os.path.join(BASE_DIR,f"media/models/_{name}.h"), "w") as text_file:
                print(c_code, file=text_file)
            m.state=True
        except Exception as e:
            print(e)
            m.state=False
            
        m.save()
        