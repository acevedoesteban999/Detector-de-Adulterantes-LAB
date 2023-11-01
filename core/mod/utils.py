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
            from tensorflow import keras
            from keras import layers
            import hexdump
            from tinymlgen import port
            from sklearn.model_selection import train_test_split
            import kerastuner as kt
            for l in _list:
                Training.objects.get(pk=l).models.add(m)
            d=[]
            l=[]
            for t in m.training_model.all():
                for measuring in t.measuring_trainig.all():
                    d.append(measuring.get_list_data()) 
                    l.append(measuring.get_predict_index())
            _in=np.array(d) 
            _out=np.array(l) 
            
            
            
            def model_builder(hp):
                model = keras.Sequential()
                
                model.add(keras.layers.Input(shape=(18, )))

                for i in range(hp.Int("num_layers", 1, 3)):
                    model.add(
                        layers.Dense(
                            units=hp.Int(f"units_{i}", min_value=32, max_value=512, step=32),
                            activation=hp.Choice("activation", ["relu", "tanh"]),
                        )
                    )
                if hp.Boolean("dropout"):
                    model.add(layers.Dropout(rate=0.25))
                
                model.add(keras.layers.Dense(5,activation="softmax"))

                hp_learning_rate = hp.Choice('learning_rate', values=[1e-2, 1e-3, 1e-4])

                model.compile(
                    optimizer=keras.optimizers.Adam(learning_rate=hp_learning_rate),
                    loss="categorical_crossentropy",
                    metrics=['accuracy']
                )

                return model
            
            
            X_train, X_test, y_train, y_test = train_test_split(_in, _out, test_size=0.2, random_state=42)
            X_train=np.expand_dims(X_train,-1).astype("float32") / 255.0
            X_test=np.expand_dims(X_test,-1).astype("float32") / 255.0
            y_train=keras.utils.to_categorical(y_train,5)
            y_test=keras.utils.to_categorical(y_test,5)
            
            def get_optim_model():    
                tuner=kt.Hyperband(
                    model_builder,
                    objective='val_accuracy',
                    max_epochs=50,
                    factor=3,
                    directory='kerastuner',
                    project_name=f"{name}H",
                )

                tuner1 = kt.RandomSearch(
                    model_builder,
                    objective='val_accuracy',
                    max_trials=5,
                    executions_per_trial=2,
                    directory='kerastuner',
                    project_name=f"{name}R"
                )
                stop_early = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5)
                tuner.search(
                    X_train,
                    y_train,
                    epochs=50,
                    validation_split=0.2,
                    validation_data=(X_test,y_test),callbacks=[stop_early]
                )
                tuner1.search(
                    X_train,
                    y_train,
                    epochs=50,
                    validation_split=0.2,
                    validation_data=(X_test,y_test),callbacks=[stop_early]
                )
                
                best_hps:kt.HyperParameters=tuner.get_best_hyperparameters(num_trials=1)[0]
                print(best_hps.values)
                model=model_builder(best_hps)
                model.summary()
                
                best_hps1:kt.HyperParameters=tuner1.get_best_hyperparameters(num_trials=1)[0]
                model1=model_builder(best_hps1)
                print(best_hps1.values)
                model1.summary()
                
                model.fit(
                    X_train,
                    y_train,
                    epochs=100,
                    validation_split=0.2,
                    validation_data=(X_test,y_test)
                )      
                
                return model
                
            def get_static_model():     
                model = keras.Sequential()
                    
                model.add(keras.layers.Input(shape=(18, )))

                model.add(layers.Dense(32,activation="relu",))
                model.add(layers.Dense(32,activation="relu",))
                model.add(keras.layers.Dense(5,activation="softmax"))

                model.compile(
                    optimizer=keras.optimizers.Adam(learning_rate=0.001),
                    loss="categorical_crossentropy",
                    metrics=['accuracy']
                )
                model.fit(
                    X_train,
                    y_train,
                    epochs=100,
                    validation_split=0.2,
                    validation_data=(X_test,y_test)
                )      
                return model
            model=get_static_model()
            # # Evaluar el modelo en los datos de prueba
            #loss, accuracy = model.evaluate(X_test, y_test)

            # # Realizar predicciones con el modelo entrenado
            #predictions = model.predict(X_test)

            # # Imprimir resultados
            #print("Loss:", loss)
            #print("Accuracy:", accuracy)
            #print("Predictions:", predictions)
            _name=name.replace(' ','_')
            model.save(os.path.join(BASE_DIR,f"media/models/{_name}.keras"))
            model.save_weights(os.path.join(BASE_DIR,f"media/models/{_name}_W.keras"))
            #c_code = port(model, pretty_print=True)
            converter = tf.lite.TFLiteConverter.from_keras_model(model)
            converter.optimizations = [tf.lite.Optimize.OPTIMIZE_FOR_SIZE]
            tflite_model = converter.convert()
            with open(os.path.join(BASE_DIR,f"media/models/{_name}"), "wb") as text_file:
                text_file.write(tflite_model)
            
            m.state=True
        except Exception as e:
            print("Error:",e)
            m.state=False
            
        m.save()
        