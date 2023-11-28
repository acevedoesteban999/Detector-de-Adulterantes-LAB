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
        p=Prediction.objects.create(
            name=name,
        )    
        measuring=MeasuringI2C(name,prediction="P")
        pd=PredictionData.objects.create(
            prediction=p,
            measuring=measuring
        )
        
        from tensorflow import keras
        import numpy as np
        _name=Model.objects.get(pk=_model_pk).name.replace(' ','_')
        model: keras.Sequential= keras.models.load_model(os.path.join(BASE_DIR,f"media/models/{_name}.keras"))
        model.load_weights(os.path.join(BASE_DIR,f"media/models/{_name}_W.keras"))
        predict_class=model.predict(np.array(measuring.get_list_data(),dtype=float).reshape(1,18)).argmax()
        pd.predict=PredictionChoices[predict_class][0]
        pd.save()   
        p.state=True
        BinnacleMessages.info("Prediction Thread",f"OK-----name: {name}")
    except Exception as e:
        BinnacleMessages.error(e)
        p.state=False
    p.save()
    #p.save_base(raw=True)            
    
def prediction_thread1(name,_model_pk,_train_pk):
    try:
        p=Prediction.objects.create(
            name=name,
        )    
        
        from tensorflow import keras
        import numpy as np
        _name=Model.objects.get(pk=_model_pk).name.replace(' ','_')
        model: keras.Sequential= keras.models.load_model(os.path.join(BASE_DIR,f"media/models/{_name}.keras"))
        model.load_weights(os.path.join(BASE_DIR,f"media/models/{_name}_W.keras"))
        
        for meas in Training.objects.get(pk=_train_pk).measuring_trainig.all():
            pd=PredictionData.objects.create(
                prediction=p,
                measuring=meas,
            )
            predict_class=model.predict(np.array(meas.get_list_data(),dtype=float).reshape(1,18)).argmax()
            pd.predict=PredictionChoices[predict_class][0]
            pd.save()
        p.state=True
        BinnacleMessages.info("Prediction Thread",f"OK-----name: {name}")
    except Exception as e:
        BinnacleMessages.error(e)
        p.state=False
    p.save()            