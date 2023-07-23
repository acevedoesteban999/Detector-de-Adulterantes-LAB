from django import forms
from core.user.models import User

class UserForm(forms.ModelForm):
    image=forms.ImageField(required=False)
    #first_name=forms.CharField(required=True)
    class Meta:
        model=User
        fields = 'first_name','username','email', 'password', 'image'
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control','placeholder': 'Ingrese un nombre'}),
            'username': forms.TextInput(attrs={'class':'form-control','placeholder': 'Ingrese un username'}),
            'email': forms.TextInput(attrs={'class':'form-control','placeholder': 'Ingrese su correo electrónico'}),
            'password': forms.PasswordInput(render_value=True,attrs={'class':'form-control','placeholder': 'Ingrese la contraseña'}),
            'image':forms.FileInput(attrs={'class':'form-control'})
        }
        
    def save(self):    
        
        model=super().save(commit=False)
        #model.
        return model
        