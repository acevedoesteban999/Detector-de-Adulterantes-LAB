import sys
import threading 
PredictionChoices=[
    ('1','100%'),
    ('7','75%'),
    ('5','50%'),
    ('2','25%'),
    ('0','0%'),
    ('N','Ninguna'),
    ('C','CSV'),
    ('M','Multi'),
    ('P',"Pred")
]
def is_at_migrations():
    return ('makemigrations' in sys.argv or 'migrate' in sys.argv)

def thread_is_alive(thred_name):  
    for t in threading.enumerate():
        if t.name == thred_name and t.is_alive():
            return True
    return False
        

          