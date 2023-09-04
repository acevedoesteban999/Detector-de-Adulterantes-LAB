from django import forms
import ipaddress
import socket   
from django.core.validators import validate_ipv4_address
from datetime import date,datetime

class NetWorkForm(forms.Form):
    ip=forms.GenericIPAddressField(initial=socket.gethostbyname(socket.gethostname()),widget=forms.TextInput(attrs={'class':'form-control'}))
    mak=forms.GenericIPAddressField(initial="0.0.0.0",widget=forms.TextInput(attrs={'class':'form-control'}))
    get=forms.GenericIPAddressField(initial="0.0.0.0",widget=forms.TextInput(attrs={'class':'form-control'}))
        
    def save(self):
        print(self.data.get('ip'),self.data.get('mak'),self.data.get('get')) 
        
class DateForm(forms.Form):
    date=forms.DateField(initial=date.today().strftime("%Y-%m-%d"),widget=forms.DateInput(attrs={'type':'date','class':'form-control'}))
    time=forms.TimeField(initial=datetime.now().strftime("%H:%M"),widget=forms.TimeInput(attrs={'type':'time','class':'form-control'}))
        
    def save(self):

        # Obtener la fecha y hora actual
        # now = datetime.datetime.now()

        # # Crear una cadena con el formato de fecha y hora deseado
        # date_string = now.strftime("%Y-%m-%d")
        # time_string = now.strftime("%H:%M:%S")

        # # Ejecutar el comando 'date' de Linux para configurar la fecha y hora
        # subprocess.call(["sudo", "date", "-s", date_string])
        # subprocess.call(["sudo", "date", "-s", time_string])
        print(self.data.get('date'),self.data.get('time'))