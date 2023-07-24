from django import forms
from core.user.models import User
from django.contrib.auth.models import Group

def get_list_groups():
    list=[]
    for group in Group.objects.all():
        list.append((group.name,group.name))
    return list

class UserForm(forms.ModelForm):
    image=forms.ImageField(required=False)
    groups = forms.ChoiceField(
        widget=forms.Select(attrs={'class':'form-control'}),
        choices=get_list_groups(),
    )
    #first_name=forms.CharField(required=True)
    class Meta:
        model=User
        fields = 'first_name','username','email', 'password', 'image','groups'
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control','placeholder': 'Ingrese un nombre'}),
            'username': forms.TextInput(attrs={'class':'form-control','placeholder': 'Ingrese un username'}),
            'email': forms.TextInput(attrs={'class':'form-control','placeholder': 'Ingrese su correo electrónico'}),
            'password': forms.PasswordInput(render_value=True,attrs={'class':'form-control','placeholder': 'Ingrese la contraseña'}),
            'image':forms.FileInput(attrs={'class':'form-control'}),
        }
        
    def save(self, commit=True):
        try:
            user = super(UserForm, self).save(commit=False)
            user.set_password(self.cleaned_data["password"])
            user.save()
            user.groups.clear()
            g=Group.objects.get(name=self.cleaned_data.get('groups'))
            user.groups.add(g)
            
        except:
            pass
        
        return user
        