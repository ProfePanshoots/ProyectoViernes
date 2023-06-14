from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class ProductoForm(ModelForm):
    nombre = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Ingrese Nombre"}))
    precio = forms.IntegerField(min_value=500,widget=forms.NumberInput(attrs={"placeholder":"Ingrese Precio"}))
    stock = forms.IntegerField(min_value=0,widget=forms.NumberInput(attrs={"placeholder":"Ingrese Stock"}))
    descripcion = forms.CharField(min_length=10,max_length=200,widget=forms.Textarea(attrs={"rows":4}))
    created_at = forms.DateTimeField(widget=forms.widgets.DateTimeInput(attrs={'type': 'date'}))
    update_at = forms.DateTimeField(widget=forms.widgets.DateTimeInput(attrs={'type': 'date'}))
    
    class Meta:
        model = Producto
        fields = '__all__'

#Para obtener modelo 


class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = CustomUser
        fields = ['username',"first_name","last_name","email","password1","password2"]


class SubscripcionForm(forms.ModelForm):
    class Meta:
        model = Subscripciones
        fields = ['suscrito']