from core.as7265x import AS7265X
from .models import Training
#from core.meas.models import Measuring,MeasuringData
from core.meas.utils import MeasuringI2C
import time

def train_thread(name,count,prediction):
    try:
        tr,created=Training.objects.get_or_create(name=name)
        tr.state=None
        if created == True:
            tr.predict=prediction
        else:
            tr.predict="M"
        __count=tr.count
        tr.count+=count
        tr.save()
        for _count in range(int(count)):
            MeasuringI2C(f"TR~{tr.name}~{__count+_count}",tr,prediction)
        tr.state=True
    except:
        tr.state=False
    tr.save()

# def TrainingI2C(name,count,prediction="N"):
#     tr,created=Training.objects.get_or_create(name=name)
#     if created == True:
#         tr.predict=prediction
#     else:
#         tr.predict="M"
#     __count=tr.count
#     tr.count+=count
#     tr.save()
#     # tr=Training.objects.create(
#     #     name=name,
#     #     count=count,
#     #     predict=prediction,
#     # )
#     for _count in range(int(count)):
#         MeasuringI2C(f"TR~{tr.name}~{__count+_count}",tr,prediction)
    
        