from core.meas.models import MeasuringData,Measuring
from core.tra.models import Training
from core.pred.models import Prediction,PredictionData
from core.mod.models import Model
from config.utils import PredictionChoices
from config.settings import BASE_DIR
from core.meas.utils import MeasuringI2C
import os
from core.binn.models import  BinnacleMessages
def prediction_thread(name,_model_pk):
    try:
        _m=Model.objects.get(pk=_model_pk)
        
        p=Prediction.objects.create(
            name=name,
            model=_m,
        )    
        measuring=MeasuringI2C(name,prediction="P")
        pd=PredictionData.objects.create(
            prediction=p,
            measuring=measuring
        )
        
        from tensorflow import keras
        import numpy as np
        _name=_m.name.replace(' ','_')
        model: keras.Sequential= keras.models.load_model(os.path.join(BASE_DIR,f"media/models/{_name}.keras"))
        model.load_weights(os.path.join(BASE_DIR,f"media/models/{_name}_W.keras"))
        
        data=np.array([measuring.get_list_data()])
        cla=model.predict(data)
        pd.predict=PredictionChoices[cla.argmax()][0]
        pd.prdict_value=cla.max()
        pd.save()   
        p.state=True
        BinnacleMessages.info("Prediction Thread",f"OK-----name: {name}")
    except Exception as e:
        print(e)
        BinnacleMessages.error(e)
        p.state=False
    p.save()          
    
def prediction_thread1(name,_model_pk,_train_pk):
    try:
        _m=Model.objects.get(pk=_model_pk)
        p=Prediction.objects.create(
            name=name,
            model=_m,
        )    
        
        from tensorflow import keras
        import numpy as np
        _name=_m.name.replace(' ','_')
        model: keras.Sequential= keras.models.load_model(os.path.join(BASE_DIR,f"media/models/{_name}.keras"))
        model.load_weights(os.path.join(BASE_DIR,f"media/models/{_name}_W.keras"))
        
        for meas in Training.objects.get(pk=_train_pk).measuring_trainig.all():
            pd=PredictionData.objects.create(
                prediction=p,
                measuring=meas,
            )
            data=np.array([meas.get_list_data()])
            cla=model.predict(data)
            pd.predict=PredictionChoices[cla.argmax()][0]
            pd.prdict_value=cla.max()
            pd.save()
        p.state=True
        BinnacleMessages.info("Prediction Thread",f"OK-----name: {name}")
    except Exception as e:
        BinnacleMessages.error(e)
        p.state=False
    p.save()            