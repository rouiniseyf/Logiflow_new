from django import forms
from django.forms import ModelForm 
from .models import *
from django.core.exceptions import NON_FIELD_ERRORS
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
import datetime
from reference.models import Client, Transitaire
class UploadFileForm(forms.Form):
    file = forms.FileField()


class GrosForm(ModelForm):
    
    class Meta:
        model = Gros
        fields = '__all__'
        exclude = ('gros','bareme')
        widgets = {
            'numero' : forms.TextInput(attrs={'class':'form-control shadow-none'}),
            'escale' : forms.TextInput(attrs={'class':'form-control shadow-none'}),
            'accostage' : forms.DateInput(attrs={'type':'date' ,'class':'form-control shadow-none','min': '2018-01-01',}),
            'navire' : forms.Select(attrs={'class':'form-control shadow-none'}),                      
            'armateur' : forms.Select(attrs={'class':'form-control shadow-none'}),                      
            'consignataire' : forms.Select(attrs={'class':'form-control shadow-none'}),                      
            'port_emission' : forms.Select(attrs={'class':'form-control shadow-none'}),                      
            'port_reception' : forms.Select(attrs={'class':'form-control shadow-none'}),                      
            'methode_calcule' : forms.Select(attrs={'class':'form-control shadow-none'}),  
            'regime' : forms.Select(attrs={'class':'form-control shadow-none'}),  
          }
        labels = {
            "port_emission": "Port d'emission",
            "port_reception": "Port de réceprion",
            "methode_calcule": "Methode de calcule",
        }

class ArticleForm(ModelForm):
    
    class Meta:
        model = Article
        fields = '__all__'
        exclude = ('transitaire','date_depotage','depote','observation_depotage')
        widgets = {
            'gros' : forms.Select(attrs={'class':'form-control shadow-none', 'readonly':True}),
            'numero' : forms.NumberInput(attrs={'class':'form-control shadow-none'}),
            'bl' : forms.TextInput(attrs={'class':'form-control shadow-none'}),
            'client' : forms.Select(attrs={'class':'form-control shadow-none'}), 
            'groupage' : forms.CheckboxInput(attrs={'class':'form-check-input shadow-none'}),
            'designation' : forms.TextInput(attrs={'class':'form-control shadow-none'}),
        }

        forms.ModelChoiceField(Client.objects.order_by('raison_sociale'))


    def clean_designation(self):
        return self.cleaned_data['designation'].upper()

    def clean_bl(self):
        return self.cleaned_data['bl'].upper()

class TcForm(ModelForm):
    
    class Meta:
        model = Tc
        fields = ['article','tc','tar','type_tc','poids','dangereux','frigo']
        widgets = {
            'article' : forms.Select(attrs={'class':'form-control shadow-none', 'readonly':True}),
            'tc' : forms.TextInput(attrs={'class':'form-control shadow-none'}),
            'tar' : forms.TextInput(attrs={'class':'form-control shadow-none'}),
            'type_tc' : forms.Select(attrs={'class':'form-control shadow-none'}), 
            'poids' : forms.NumberInput(attrs={'class':'form-control shadow-none','step': 0.01}), 
            'dangereux' : forms.CheckboxInput(attrs={'class':'form-check-input shadow-none'}),
            'frigo' : forms.CheckboxInput(attrs={'class':'form-check-input shadow-none'})

        }
        labels = {
                "type_tc": "Type",
            }   
            
class SearchForm(forms.Form):
    search = forms.CharField() 

class FilterGrosArticleForm(forms.Form):
    search = forms.CharField() 
    gros = forms.IntegerField() 
    article = forms.IntegerField()

class BulletinsEscortForm(ModelForm):
    
    class Meta:
        model = BulletinsEscort
        fields = ['numero','date_creation','gros' ]
        widgets = {
            'numero' : forms.TextInput(attrs={'class':'form-control shadow-none disable', 'readonly':True}),
            'date_creation' : forms.DateInput(attrs={'type':'date' ,'class':'form-control shadow-none','min': '2018-01-01'}),
            'gros' : forms.Select(attrs={'class':'form-control select2 shadow-none'}), 
        }


class VisiteForm(ModelForm):
    class Meta:
        model = Visite
        fields = ['gros','article','numero','type_visite','date_visite','transitaire','badge' ]
        widgets = {
            'gros' : forms.Select(attrs={'class':'form-control shadow-none'}), 
            'article' : forms.Select(attrs={'class':'form-control shadow-none'}), 
            'numero' : forms.TextInput(attrs={'class':'form-control shadow-none disable', 'readonly':True}),
            'type_visite' : forms.Select(attrs={'class':'form-control shadow-none'}), 
            'date_visite' : forms.DateInput(attrs={'type':'date' ,'class':'form-control shadow-none','min': '2018-01-01'}),
            'transitaire' : forms.Select(attrs={'class':'form-control shadow-none'}), 
            'badge' : forms.TextInput(attrs={'class':'form-control shadow-none disable'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['article'].queryset = Article.objects.none()



class VisiteFacturationForm(ModelForm):
    class Meta:
        model = Visite
        fields = ['gros','article','numero','type_visite','date_visite','transitaire','badge' ]
        widgets = {
            'gros' : forms.TextInput(attrs={'class':'form-control shadow-none', 'readonly':True}), 
            'article' : forms.TextInput(attrs={'class':'form-control shadow-none', 'readonly':True}), 
            'numero' : forms.TextInput(attrs={'class':'form-control shadow-none disable', 'readonly':True}),
            'type_visite' : forms.Select(attrs={'class':'form-control shadow-none'}), 
            'date_visite' : forms.DateInput(attrs={'type':'date' ,'class':'form-control shadow-none','min': '2018-01-01'}),
            'transitaire' : forms.Select(attrs={'class':'form-control shadow-none'}), 
            'badge' : forms.TextInput(attrs={'class':'form-control shadow-none disable'}),
        }
        

        
class SousArticleForm(ModelForm):
    class Meta:
        model = SousArticle
        fields = ['numero','tc','bl','volume','nombre_colis','surface','quantite','poids','description','client',]
        exclude = ['box', ]
        widgets = {
            'numero' : forms.TextInput(attrs={'class':'form-control shadow-none'}), 
            'tc' : forms.Select(attrs={'class':'form-control shadow-none disable', 'readonly':True}), 
            'bl' : forms.TextInput(attrs={'class':'form-control shadow-none'}), 
            'volume' : forms.NumberInput(attrs={'class':'form-control shadow-none'}),
            'nombre_colis' : forms.NumberInput(attrs={'class':'form-control shadow-none'}), 
            'surface' : forms.NumberInput(attrs={'class':'form-control shadow-none'}),
            'quantite' : forms.NumberInput(attrs={'class':'form-control shadow-none'}), 
            'poids' : forms.NumberInput(attrs={'class':'form-control shadow-none disable'}),
            'client' : forms.Select(attrs={'class':'form-control shadow-none disable'}),
            'description' : forms.TextInput(attrs={'class':'form-control shadow-none disable'}),
        }

    def clean_description(self):
        return self.cleaned_data['description'].upper()


class PositionForm(ModelForm):
    class Meta:
        model = Position
        fields = ['tc','parc','zone','ligne','range','garbage',]
        widgets = {
            'parc' : forms.Select(attrs={'class':'form-control shadow-none'}), 
            'zone' : forms.Select(attrs={'class':'form-control shadow-none'}), 
            'tc' : forms.TextInput(attrs={'class':'form-control shadow-none disable', 'readonly':True}), 
            'ligne' : forms.NumberInput(attrs={'class':'form-control shadow-none'}),
            'range' : forms.NumberInput(attrs={'class':'form-control shadow-none'}), 
            'garbage' : forms.NumberInput(attrs={'class':'form-control shadow-none'}),
        }

