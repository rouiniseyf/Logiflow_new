from django import forms
from django.forms import ModelForm 
from .models import *
from django.core.exceptions import NON_FIELD_ERRORS
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
import datetime


class PortForm(ModelForm):
    
    class Meta:
        model = Port
        fields = '__all__'
        widgets = {
            'raison_sociale' : forms.TextInput(attrs={'class':'form-control shadow-none','style': 'text-transform:lowercase;'}),
            'code' : forms.TextInput(attrs={'class':'form-control shadow-none'}),
            'pays' : forms.Select(attrs={'class':'form-control shadow-none'}),      
          }
        labels = {
            "raison_social": "Raison Social",
        }

    def clean_raison_sociale(self):
        return self.cleaned_data['raison_sociale'].upper()

class NavireForm(ModelForm):
    
    class Meta:
        model = Navire
        fields = '__all__'
        widgets = {
            'nom' : forms.TextInput(attrs={'class':'form-control shadow-none'}),
            'code' : forms.TextInput(attrs={'class':'form-control shadow-none'}),
          }


    def clean_nom(self):
        return self.cleaned_data['nom'].upper()

class ArmateurForm(ModelForm):
    
    class Meta:
        model = Armateur
        fields = '__all__'
        widgets = {
            'raison_sociale' : forms.TextInput(attrs={'class':'form-control shadow-none'}),
            'code' : forms.TextInput(attrs={'class':'form-control shadow-none'}),
        }

    def clean_raison_sociale(self):
        return self.cleaned_data['raison_sociale'].upper()

class ConsignataireForm(ModelForm):
    class Meta:
        model = Consignataire
        fields = '__all__'
        widgets = {
            'raison_sociale' : forms.TextInput(attrs={'class':'form-control shadow-none'}),
            'code' : forms.TextInput(attrs={'class':'form-control shadow-none'}),
        }

    def clean_raison_sociale(self):
        return self.cleaned_data['raison_sociale'].upper()

class TypeTcForm(ModelForm):
    
    class Meta:
        model = Type
        fields = '__all__'
        widgets = {
            'designation' : forms.TextInput(attrs={'class':'form-control shadow-none'}),
        }


class TransitaireForm(ModelForm):
    class Meta:
        model = Transitaire
        fields = ['raison_sociale','adress','email','tel' ]
        widgets = {
            'raison_sociale' : forms.TextInput(attrs={'class':'form-control shadow-none disable' }),
            'adress' : forms.TextInput(attrs={'class':'form-control shadow-none'}),
            'email' : forms.EmailInput(attrs={'class':'form-control shadow-none'}), 
            'tel' : forms.TextInput(attrs={'class':'form-control shadow-none'}), 
        }

    def clean_raison_sociale(self):
        return self.cleaned_data['raison_sociale'].upper()    

class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = '__all__' 
        widgets = {
            'raison_sociale' : forms.TextInput(attrs={'class':'form-control shadow-none' }),
            'adress' : forms.TextInput(attrs={'class':'form-control shadow-none'}),
            'tel' : forms.EmailInput(attrs={'class':'form-control shadow-none'}), 
            'email' : forms.EmailInput(attrs={'class':'form-control shadow-none'}), 
            'code' : forms.TextInput(attrs={'class':'form-control shadow-none'}), 
            'RC' : forms.TextInput(attrs={'class':'form-control shadow-none'}), 
            'NIF' : forms.TextInput(attrs={'class':'form-control shadow-none'}), 
            'AI' : forms.TextInput(attrs={'class':'form-control shadow-none'}), 
            'NIS' : forms.TextInput(attrs={'class':'form-control shadow-none'}), 
            'soumis_tva' : forms.CheckboxInput(attrs={'class':'form-check-input shadow-none'}),

        }

    def clean_raison_sociale(self):
        return self.cleaned_data['raison_sociale'].upper()  


class AgentForm(ModelForm):
    
    class Meta:
        model = Agent
        fields = '__all__'
        widgets = {
            'nom' : forms.TextInput(attrs={'class':'form-control shadow-none'}),
            'prenom' : forms.TextInput(attrs={'class':'form-control shadow-none'})
        }
        labels = {
            "nom": "Nom",
            "prenom": "Prenom",
        }

    def clean_raison_sociale(self):
        return self.cleaned_data['raison_sociale'].upper()