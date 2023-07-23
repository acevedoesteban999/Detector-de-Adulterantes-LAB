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
        print(self.data.get('date'),self.data.get('time'))