from core.meas.models import MeasuringData
from core.pred.models import Prediction
from core.mod.models import Model
from config.utils import PredictionChoices
from config.settings import BASE_DIR
from core.meas.utils import MeasuringI2C
import os
def prediction_thread(name,_model_pk):
    try:
        measuring=MeasuringI2C(name)
        p=Prediction(measuring_ptr=measuring)
        p.save_base(raw=True)            
        from tensorflow import keras
        import numpy as np
        _name=Model.objects.get(pk=_model_pk).name.replace(' ','_')
        model: keras.Sequential= keras.models.load_model(os.path.join(BASE_DIR,f"media/models/{_name}.keras"))
        model.load_weights(os.path.join(BASE_DIR,f"media/models/{_name}_W.keras"))
        predict_class=model.predict(np.array(measuring.get_list_data(),dtype=float).reshape(1,18)).argmax()
        measuring.predict=PredictionChoices[predict_class][0]
        measuring.save()
        p.state=True
        
    except Exception as e:
        print("Error:",e)
        p.state=False
    p.save_base(raw=True)            