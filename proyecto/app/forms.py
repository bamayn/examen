from django import forms
from .models import Persona, Genero,Usuario, Venta
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class Usuario(forms.ModelForm):
    #use_required_attribute = False  
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['foto'].required = False


    class Meta:
        model = Usuario
        fields = '__all__'

class usuarioRegistro(UserCreationForm):
    
    
    class Meta:
        model= User
        fields = ['username','first_name','last_name',"email",'password1','password2']

class usuarioEdit(UserCreationForm):
    
    
    class Meta:
        model= User
        fields = ['username','first_name','last_name',"email","is_staff"]

class VentaForm(forms.ModelForm):

    class Meta:
        model = Venta
        fields = '__all__'