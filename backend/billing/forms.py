from django import forms
from django.forms import ModelForm 
from .models import *
from django.core.exceptions import NON_FIELD_ERRORS
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
import datetime
from app.models import *


class ProformaForm(ModelForm):
    class Meta:
        model = Proforma
        fields = "__all__"
        exclude = ('HT','TVA','TTC','TR', 'valide' ,'trashed')
        widgets = {
            'numero' : forms.TextInput(attrs={'class':'form-control shadow-none bg-light disable', 'readonly':True}), 
            'gros' : forms.TextInput(attrs={'class':'form-control shadow-none bg-light' , 'readonly':True}),
            'article' : forms.TextInput(attrs={'class':'form-control shadow-none bg-light' , 'readonly':True}), 
            'date_proforma' : forms.DateInput(attrs={'type':'date' ,'class':'form-control shadow-none','min': '2018-01-01'}),
            'tva' : forms.CheckboxInput(attrs={'class':'form-check-input shadow-none'}),
            'entreposage' : forms.CheckboxInput(attrs={'class':'form-check-input shadow-none'}),
            'remise' : forms.CheckboxInput(attrs={'class':'form-check-input shadow-none'}),
            'REMISE' : forms.NumberInput(attrs={'class':'form-control shadow-none'}), 
            'debeur' : forms.CheckboxInput(attrs={'class':'form-check-input shadow-none'}),
            'DEBEUR' : forms.NumberInput(attrs={'class':'form-control shadow-none'}),
        }


        labels = {
                "date_proforma": "Date",
                "valeur_remise": "Pourcentage < 100 ou Montant > 100",
                "tva": "TVA",
                "remise": "Remise ( Pourcentage or Montant fix )",
            } 
        
class ProformaGroupageForm(ModelForm):
    class Meta:
        model = ProformaGroupage
        fields = "__all__"
        exclude = ('HT','TVA','TTC','TR', 'valide' ,'trashed','enterposage')
        widgets = {
            'numero' : forms.TextInput(attrs={'class':'form-control shadow-none bg-light disable', 'readonly':True}), 
            'gros' : forms.TextInput(attrs={'class':'form-control shadow-none bg-light', 'readonly':True}),
            'article' : forms.TextInput(attrs={'class':'form-control shadow-none bg-light', 'readonly':True}), 
            'sous_article' : forms.TextInput(attrs={'class':'form-control shadow-none bg-light', 'readonly':True}), 
            'date_proforma' : forms.DateInput(attrs={'type':'date' ,'class':'form-control shadow-none','min': '2018-01-01'}),
            'tva' : forms.CheckboxInput(attrs={'class':'form-check-input shadow-none'}),
            'remise' : forms.CheckboxInput(attrs={'class':'form-check-input shadow-none'}),
            'REMISE' : forms.NumberInput(attrs={'class':'form-control shadow-none'}), 
            'debeur' : forms.CheckboxInput(attrs={'class':'form-check-input shadow-none'}),
            'DEBEUR' : forms.NumberInput(attrs={'class':'form-control shadow-none'}), 
        }


        labels = {
                "date_proforma": "Date",
                "valeur_remise": "Pourcentage < 100 ou Montant > 100",
                "tva": "TVA",
                "remise": "Remise ( Pourcentage or Montant fix )",
                "debeur": "DEBEUR"
            } 
        

class FactureGroupageForm(ModelForm):
    class Meta:
        model = FactureGroupage
        fields = "__all__"
        exclude = ('HT','TVA','TTC','paid','timber','TR','DEBEUR')
        widgets = {
            'numero' : forms.TextInput(attrs={'class':'form-control shadow-none bg-light', 'readonly':True}), 
            'proforma' : forms.TextInput(attrs={'class':'form-control shadow-none bg-light','readonly':True}),
            'a_terme' : forms.CheckboxInput(attrs={'class':'form-check-input shadow-none'}),
        }


class FactureLibreForm(ModelForm):
    class Meta:
        model = FactureLibre
        fields = "__all__"
        exclude = ('numero','HT','TVA','TTC','TR','timber','paid')
        widgets = {
            'client' : forms.Select(attrs={'class':'form-control shadow-none'}),
            'date_facture' : forms.DateInput(attrs={'type':'date' ,'class':'form-control shadow-none','min': '2018-01-01'}),
            'date' : forms.DateInput(attrs={'type':'date' ,'class':'form-control shadow-none','min': '2018-01-01'}),
            'type_dossier' : forms.TextInput(attrs={'class':'form-control shadow-none'}),
            'ref' : forms.TextInput(attrs={'class':'form-control shadow-none'}),
            'designation' : forms.TextInput(attrs={'size': 10,'class':'form-control shadow-none'}),
            'tva' : forms.CheckboxInput(attrs={'class':'form-check-input shadow-none'}),
            'remise' : forms.CheckboxInput(attrs={'class':'form-check-input shadow-none'}),
            'REMISE' : forms.NumberInput(attrs={'class':'form-control shadow-none'}), 
        }

        labels = {
                "date_proforma": "Date",
                "valeur_remise": "Pourcentage < 100 ou Montant > 100",
                "tva": "TVA",
                "remise": "Remise ( Pourcentage or Montant fix )",
                "ref": "V/Réf",
            }    


class FactureForm(ModelForm):
    class Meta:
        model = Facture
        fields = "__all__"
        exclude = ('HT','TVA','TTC','paid','timber','TR','DEBEUR')
        widgets = {
            'numero' : forms.TextInput(attrs={'class':'form-control shadow-none bg-light', 'readonly':True}), 
            'proforma' : forms.TextInput(attrs={'class':'form-control shadow-none bg-light','readonly':True}),
            'a_terme' : forms.CheckboxInput(attrs={'class':'form-check-input shadow-none'}),
        }

class FactureComplementaireForm(ModelForm):
    class Meta:
        model = FactureComplementaire
        fields = "__all__"
        exclude = ('HT','TVA','TTC','paid','timber','TR','numero','full_number')
        widgets = {
            'facture' : forms.Select(attrs={'class':'form-control shadow-none bg-light', 'readonly':True}),
            'tva' : forms.CheckboxInput(attrs={'class':'form-check-input shadow-none'}),           
        }


class FactureAvoireForm(ModelForm):
    class Meta:
        model = FactureAvoire
        fields = "__all__"
        exclude = ('HT','TVA','TTC','paid','timber','TR','numero','full_number')
        widgets = {
            'facture' : forms.Select(attrs={'class':'form-control shadow-none bg-light', 'readonly':True}),
            'tva' : forms.CheckboxInput(attrs={'class':'form-check-input shadow-none'}),           
        }

class BonSortieForm(ModelForm): 
    class Meta: 
        model = BonSortie
        fields = "__all__"
        exclude = ('date_sortie', 'date_creation')
        widgets = {
            'facture' : forms.TextInput(attrs={'class':'form-control shadow-none bg-light', 'readonly':True}),
            'numero' : forms.TextInput(attrs={'class':'form-control shadow-none bg-light', 'readonly':True}),
            'd10' : forms.TextInput(attrs={'class':'form-control shadow-none'}),           
            'badge' : forms.TextInput(attrs={'class':'form-control shadow-none'}),           
        }         