from core.as7265x import AS7265X
from .models import Training
from config.utils import PredictionChoices
from core.meas.models import Measuring,MeasuringData
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


def csv_thread(_1f,count,csv_read,name):
    def save1(count,csv_read,name):
        try:
            t=Training.objects.create(
                name=name,
                predict="C",
            )
            _count=count
            #_r=csv.read().decode("utf-8").splitlines()[1:_count]
            _r=csv_read.decode("utf-8").splitlines()[1:_count]
            rows=[]
            for r in _r:
                rows.append(r.split(',')) 
            for count in range(len(rows)):
                print(count)
                prediction=PredictionChoices[int(rows[count][1])-1][0]
                m=Measuring.objects.create(
                    name=f"T~{name}~{count}",
                    training=t,
                    predict=prediction
                )
                
                t.count+=1
                for c,d in enumerate(rows[count],start=-2):
                    if c<0:
                        continue
                    MeasuringData.objects.create(
                        chanel= Measuring.chanels()[c],
                        value=float(d),
                        measuring=m
                    )
            print("True")
            t.state=True
        except:
            print("False")
            t.state=False
        t.save() 
    try:
        if _1f==True:
            return save1(count,csv_read,name)
        t=Training.objects.create(
            name=name,
            predict="C",
        )
        _count=count
        #_r=csv.read().decode("utf-8").splitlines()[1:_count]
        _r=csv_read.decode("utf-8").splitlines()[1:_count]

        rows=[]
        for r in _r:
            rows.append(r.split(',')) 
        t=Training.objects.create(
            name=name,
            predict="C",
            )
        for count in range(len(rows)):
            prediction=PredictionChoices[int(rows[count][18])][0]
        
        m=Measuring.objects.create(
            name=f"T~{name}~{count}",
            training=t,
            predict=prediction
        )
        t.count+=1
        for c,d in enumerate(rows[count]):
            if c==18:
                break
            MeasuringData.objects.create(
                chanel= Measuring.chanels()[c],
                value=float(d),
                measuring=m
            )
        t.state=True
    except:
        t.state=False
    t.save() 
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
    
        