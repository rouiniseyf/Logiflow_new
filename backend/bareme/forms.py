from django import forms
from django.forms import ModelForm 
from .models import *
from django.core.exceptions import NON_FIELD_ERRORS
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
import datetime



class BaremeForm(ModelForm):
    
    class Meta:
        model = Bareme
        fields = '__all__'
        exclude = ('gros','bareme')
        widgets = {
            'designation' : forms.TextInput(attrs={'class':'form-control shadow-none'}),
            'starting_date' : forms.DateInput(attrs={'type':'date' ,'class':'form-control shadow-none','min': '2018-01-01'}),
            'ending_date' : forms.DateInput(attrs={'type':'date' ,'class':'form-control shadow-none','min': '2018-01-01'}),
        }
        labels = {
            "designation": "Designation",
            "starting_date": "Début",
            "ending_date": "Fin",
        }

