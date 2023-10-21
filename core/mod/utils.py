from core.mod.models import Model
from core.tra.models import Training
from config.settings import BASE_DIR
import os

def trin_model_thread(name,_list):
        try:
            import time
            m=Model.objects.create(
                name=name,
            )
            import numpy as np
            import tensorflow as tf
            import hexdump
            from tinymlgen import port
            for l in _list:
                Training.objects.get(pk=l).models.add(m)
            d=[]
            l=[]
            for t in m.training_model.all():
                for measuring in t.measuring_trainig.all():
                    d.append(measuring.get_list_data()) 
                    l.append(measuring.get_predict_index())
            _in=np.array(d,dtype=float)
            _out=np.array(l,dtype=int)
            
            input = tf.keras.Input(shape=(18,))
            x = tf.keras.layers.Dense(30, activation=tf.nn.relu)(input)
            x = tf.keras.layers.Dense(30, activation=tf.nn.relu)(x)
            output = tf.keras.layers.Dense(5,activation=tf.nn.softmax)(x)
            model=tf.keras.Model(input, output)
            
            model.compile(
                optimizer=tf.keras.optimizers.Adam(0.1),
                loss="mean_squared_error",
                metrics=['accuracy'],
                
            )
            model.fit(
                _in,
                _out,
                epochs=10,
                verbose=False,
            )
            _name=name.replace(' ','_')
            model.save(os.path.join(BASE_DIR,f"media/models/{_name}.keras"))
            model.save_weights(os.path.join(BASE_DIR,f"media/models/{_name}_W.keras"))
            #c_code = port(model, pretty_print=True)
            converter = tf.lite.TFLiteConverter.from_keras_model(model)
            converter.optimizations = [tf.lite.Optimize.OPTIMIZE_FOR_SIZE]
            tflite_model = converter.convert()
            with open(os.path.join(BASE_DIR,f"media/models/{_name}.edbm"), "wb") as text_file:
                text_file.write(tflite_model)
            
            
            m.state=True
        except Exception as e:
            print("Error:",e)
            m.state=False
            
        m.save()
        