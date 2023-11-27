from django import forms
import ipaddress
import socket   
from django.core.validators import validate_ipv4_address
from datetime import date,datetime
import subprocess
from core.binn.models import BinnacleMessages
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
        try:
            date=self.data.get('date')
            time=self.data.get('time')
            # Ejecutar el comando 'date' de Linux para configurar la fecha y hora
            subprocess.call(["sudo", "date", "-s", date])
            subprocess.call(["sudo", "date", "-s", time])
            BinnacleMessages.info("Change Date Tine",f"Change to: {date} {time}")
        except Exception as e:
            BinnacleMessages.error(e)
        