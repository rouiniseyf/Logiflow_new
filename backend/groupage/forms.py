from app.models import * 
from groupage.models import *
from django import forms
from django.forms import ModelForm 
from .models import *
from django.core.exceptions import NON_FIELD_ERRORS
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
import datetime
from reference.models import Client, Transitaire

class VisiteGroupageForm(ModelForm):
    class Meta:
        model = VisiteGroupage
        fields = ['gros','article','sous_article','numero','type_visite','date_visite','transitaire','badge' ]
        widgets = {
            'gros' : forms.Select(attrs={'class':'form-control shadow-none'}), 
            'article' : forms.Select(attrs={'class':'form-control shadow-none'}), 
            'sous_article' : forms.Select(attrs={'class':'form-control shadow-none'}), 
            'numero' : forms.TextInput(attrs={'class':'form-control shadow-none disable', 'readonly':True}),
            'type_visite' : forms.Select(attrs={'class':'form-control shadow-none'}), 
            'date_visite' : forms.DateInput(attrs={'type':'date' ,'class':'form-control shadow-none','min': '2018-01-01'}),
            'transitaire' : forms.Select(attrs={'class':'form-control shadow-none'}), 
            'badge' : forms.TextInput(attrs={'class':'form-control shadow-none disable'}),
            'description' : forms.TextInput(attrs={'class':'form-control shadow-none disable'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['article'].queryset = Article.objects.none()
        self.fields['sous_article'].queryset = SousArticle.objects.none()
