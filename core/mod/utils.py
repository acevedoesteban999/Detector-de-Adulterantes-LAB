from core.mod.models import Model
from core.tra.models import Training
from config.settings import BASE_DIR
import os
from core.binn.models import  BinnacleMessages

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
            from matplotlib import pyplot as plt
            from sklearn.metrics import confusion_matrix
            import seaborn as sns
            import matplotlib
            matplotlib.use('Agg')
            from config.settings import MEDIA_ROOT
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
                
                model.add(
                    layers.Dense(
                        units=hp.Int("units_0", min_value=32, max_value=256, step=32),
                        activation=hp.Choice("activation", ["relu", "tanh"]),
                    )
                )
                
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
                epochs=800
                tuner=kt.Hyperband(
                    model_builder,
                    objective='val_accuracy',
                    max_epochs=epochs,
                    factor=3,
                    directory='kerastuner',
                    project_name=f"{name}H",
                )
                stop_early = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5)
                
                tuner.search(
                    X_train,
                    y_train,
                    epochs=epochs,
                    validation_split=0.2,
                    verbose=False,
                    validation_data=(X_test,y_test),
                    callbacks=[stop_early]
                )
                print("Hyperband HyperParameters:")
                best_hps:kt.HyperParameters=tuner.get_best_hyperparameters(num_trials=1)[0]
                for k,v in best_hps.values.items(): 
                    print(k,":",v)
                model=model_builder(best_hps)
                model.summary()
                import time
                t=time.time()
                history=model.fit(
                    X_train,
                    y_train,
                    verbose=False,
                    epochs=epochs,
                    validation_split=0.2,
                    validation_data=(X_test,y_test)
                )    
                epochs_range=range(0,epochs)
                
                plt.clf()
                plt.plot(epochs_range,history.history['loss'],'r',label='Training Loss')
                plt.title("Training  Loss")
                plt.xlabel("Epochs")
                plt.ylabel("Loss")
                plt.legend()
                plt.savefig(MEDIA_ROOT+"/trains/"+f"{name}_loss.png")
                
                plt.clf()
                plt.plot(epochs_range,history.history['accuracy'],'g',label='Training Accuracy')
                plt.title("Training  Accuracy")
                plt.xlabel("Epochs")
                plt.ylabel("Accuracy")
                plt.legend()
                plt.savefig(MEDIA_ROOT+"/trains/"+f"{name}_accuracy.png")
                
                plt.clf()
                y_pred=model.predict(X_test) 
                cm=confusion_matrix(y_test.argmax(axis=1), y_pred.argmax(axis=1))
                sns.heatmap(cm, annot=True, cmap='Blues', fmt='d', cbar=False)                
                plt.title('Confusion Matrix')
                plt.xticks([])
                plt.yticks([])
                plt.savefig(MEDIA_ROOT+"/trains/"+f"{name}_confusion_matrix.png")
                
                print("Hyperband train time:")  
                print(time.time()-t)
                loss, accuracy = model.evaluate(X_test, y_test)
                print("Loss:", loss)
                print("Accuracy:", accuracy)
                print("Best Epoch: ")  
                values_accuracy=history.history['val_accuracy']
                best_epochs=values_accuracy.index(max(values_accuracy))+1
                print(best_epochs)
                

                return model                 
            def get_static_model():     
                model = keras.Sequential()
                model.add(keras.layers.Input(shape=(18, )))
                model.add(layers.Dense(224,activation="tanh",))
                model.add(keras.layers.Dense(5,activation="softmax"))

                model.compile(
                    optimizer=keras.optimizers.Adam(learning_rate=0.001),
                    loss="categorical_crossentropy",
                    metrics=['accuracy']
                )
                
                epochs=250
                t=time.time()
                history=model.fit(
                    X_train,
                    y_train,
                    epochs=epochs,
                    verbose=False,
                    validation_split=0.2,
                    validation_data=(X_test,y_test)
                )
                
                print("Train time:")  
                print(time.time()-t)
                loss, accuracy = model.evaluate(X_test, y_test)
                print("Loss:", loss)
                print("Accuracy:", accuracy)
                
                epochs_range=range(0,epochs)      
                plt.clf()
                plt.plot(epochs_range,history.history['loss'],'r',label='Training Loss')
                plt.title("Training  Loss")
                plt.xlabel("Epochs")
                plt.ylabel("Loss")
                plt.legend()
                plt.savefig(MEDIA_ROOT+"/trains/"+f"{name}_loss.png")
                
                plt.clf()
                plt.plot(epochs_range,history.history['accuracy'],'g',label='Training Accuracy')
                plt.title("Training  Accuracy")
                plt.xlabel("Epochs")
                plt.ylabel("Accuracy")
                plt.legend()
                plt.savefig(MEDIA_ROOT+"/trains/"+f"{name}_accuracy.png")
                
                plt.clf()
                y_pred=model.predict(X_test) 
                cm=confusion_matrix(y_test.argmax(axis=1), y_pred.argmax(axis=1))
                sns.heatmap(cm, annot=True, cmap='Blues', fmt='d', cbar=False)                
                plt.title('Confusion Matrix')
                plt.xticks([])
                plt.yticks([])
                plt.savefig(MEDIA_ROOT+"/trains/"+f"{name}_confusion_matrix.png")
                return model
            
            #model=get_optim_model()
            model=get_static_model()
            _name=name.replace(' ','_')
            model.save(os.path.join(BASE_DIR,f"media/models/{_name}.keras"))
            model.save_weights(os.path.join(BASE_DIR,f"media/models/{_name}_W.keras"))
            converter = tf.lite.TFLiteConverter.from_keras_model(model)
            converter.optimizations = [tf.lite.Optimize.OPTIMIZE_FOR_SIZE]
            tflite_model = converter.convert()
            with open(os.path.join(BASE_DIR,f"media/models/{_name}"), "wb") as text_file:
                text_file.write(tflite_model)
            
            
            m.state=True
            BinnacleMessages.info("ModelTrain Thread",f"OK-----name: {name}")
        except Exception as e:
            BinnacleMessages.error(e)
            m.state=False
            
        m.save()
        