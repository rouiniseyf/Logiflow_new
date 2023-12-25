from rest_framework import serializers
from .models import *
from rest_flex_fields import FlexFieldsModelSerializer
from drf_writable_nested.serializers import WritableNestedModelSerializer

class LignePrestationExportSerializer(serializers.ModelSerializer): 

    class Meta: 
        model = LignePrestation 
        fields = '__all__'
        depth = 2


class BonSortieGroupageSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = BonSortieGroupage
        fields = '__all__'


        expandable_fields = {
            'sous_article': ('app.serializers.SousArticleSerializer',{'many': False}),
            'facture': ('billing.serializers.FactureGroupageSerializer',{'many': False}),
             }



class PaiementGroupageSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = PaiementGroupage
        fields = '__all__'


        expandable_fields = {
            'facture': ('billing.serializers.FactureGroupageSerializer',{'many': False}),
            'banque': ('reference.serializers.BanqueSerializer',{'many': False}),
             }


class FactureGroupageSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = FactureGroupage
        fields = '__all__'


        expandable_fields = {
            'paiementgroupages': ('billing.serializers.PaiementGroupageSerializer',{'many': True}),
            'bonsortiegroupages': ('billing.serializers.BonSortieGroupageSerializer',{'many': True}),
            'proforma': ('billing.serializers.ProformaGroupageSerializer',{'many': False}),
             }


class LigneProformaGroupageSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = LigneProformaGroupage
        fields = '__all__'


        expandable_fields = {
            'proforma': ('billing.serializers.ProformaGroupageSerializer',{'many': False}),
            'rubrique_object': ('bareme.serializers.RubriqueSerializer',{'many': False}),
             }


class ProformaGroupageSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = ProformaGroupage
        fields = '__all__'


        expandable_fields = {
            'ligneproformagroupages': ('billing.serializers.LigneProformaGroupageSerializer',{'many': True}),
            'facturegroupages': ('billing.serializers.FactureGroupageSerializer',{'many': True}),
            'gros': ('app.serializers.GrosSerializer',{'many': False}),
            'article': ('app.serializers.ArticleSerializer',{'many': False}),
            'sous_article': ('app.serializers.SousArticleSerializer',{'many': False}),
             }


class PaiementFactureLibreSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = PaiementFactureLibre
        fields = '__all__'


        expandable_fields = {
            'facture_libre': ('billing.serializers.FactureLibreSerializer',{'many': False}),
            'banque': ('reference.serializers.BanqueSerializer',{'many': False}),
             }


class LigneFactureLibreSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = LigneFactureLibre
        fields = '__all__'


        expandable_fields = {
            'facture_libre': ('billing.serializers.FactureLibreSerializer',{'many': False}),
            'rubrique': ('bareme.serializers.RubriqueSerializer',{'many': False}),
             }


class FactureLibreSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = FactureLibre
        fields = '__all__'


        expandable_fields = {
            'lignefacturelibres': ('billing.serializers.LigneFactureLibreSerializer',{'many': True}),
            'paiementfacturelibres': ('billing.serializers.PaiementFactureLibreSerializer',{'many': True}),
            'client': ('reference.serializers.ClientSerializer',{'many': False}),
             }




class BonSortieItemSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = BonSortieItem
        fields = '__all__'


        expandable_fields = {
            'bon_sortie': ('billing.serializers.BonSortieSerializer',{'many': False}),
            'tc': ('app.serializers.TcSerializer',{'many': False}),
             }


class BonSortieSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = BonSortie
        fields = '__all__'


        expandable_fields = {
            'bonsortieitems': ('billing.serializers.BonSortieItemSerializer',{'many': True}),
            'facture': ('billing.serializers.FactureSerializer',{'many': False}),
             }



class LigneFactureAvoireSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = LigneFactureAvoire
        fields = '__all__'


        expandable_fields = {
            'facture_avoire': ('billing.serializers.FactureAvoireSerializer',{'many': False}),
             }


class FactureAvoireSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = FactureAvoire
        fields = '__all__'


        expandable_fields = {
            'lignefactureavoires': ('billing.serializers.LigneFactureAvoireSerializer',{'many': True}),
            'facture': ('billing.serializers.FactureSerializer',{'many': False}),
             }




class PaiementFactureComplementaireSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = PaiementFactureComplementaire
        fields = '__all__'


        expandable_fields = {
            'facture_complementaire': ('billing.serializers.FactureComplementaireSerializer',{'many': False}),
            'banque': ('reference.serializers.BanqueSerializer',{'many': False}),
             }


class LigneFactureComplementaireSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = LigneFactureComplementaire
        fields = '__all__'


        expandable_fields = {
            'facture_complementaire': ('billing.serializers.FactureComplementaireSerializer',{'many': False}),
             }


class FactureComplementaireSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = FactureComplementaire
        fields = '__all__'


        expandable_fields = {
            'lignefacturecomplementaires': ('billing.serializers.LigneFactureComplementaireSerializer',{'many': True}),
            'paiementfacturecomplementaires': ('billing.serializers.PaiementFactureComplementaireSerializer',{'many': True}),
            'facture': ('billing.serializers.FactureSerializer',{'many': False}),
             }


class PaiementSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = Paiement
        fields = '__all__'


        expandable_fields = {
            'facture': ('billing.serializers.FactureSerializer',{'many': False}),
            'banque': ('reference.serializers.BanqueSerializer',{'many': False}),
             }


class FactureSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = Facture
        fields = '__all__'


        expandable_fields = {
            'paiements': ('billing.serializers.PaiementSerializer',{'many': True}),
            'facturecomplementaires': ('billing.serializers.FactureComplementaireSerializer',{'many': True}),
            'factureavoires': ('billing.serializers.FactureAvoireSerializer',{'many': True}),
            'bonsorties': ('billing.serializers.BonSortieSerializer',{'many': True}),
            'proforma': ('billing.serializers.ProformaSerializer',{'many': False}),
             }


class CommandeSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = Commande
        fields = '__all__'


        expandable_fields = {
            'bon_commande': ('billing.serializers.BonCommandeSerializer',{'many': False}),
            'tc': ('app.serializers.TcSerializer',{'many': False}),
            'rubrique_object': ('bareme.serializers.RubriqueSerializer',{'many': False}),
             }


class BonCommandeSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = BonCommande
        fields = '__all__'


        expandable_fields = {
            'commandes': ('billing.serializers.CommandeSerializer',{'many': True}),
            'article': ('app.serializers.ArticleSerializer',{'many': False}),
             }


class LignePrestationArticleSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = LignePrestationArticle
        fields = '__all__'


        expandable_fields = {
            'proforma': ('billing.serializers.ProformaSerializer',{'many': False}),
            'rubrique_object': ('bareme.serializers.RubriqueSerializer',{'many': False}),
             }


class LignePrestationSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = LignePrestation
        fields = '__all__'


        expandable_fields = {
            'proforma': ('billing.serializers.ProformaSerializer',{'many': False}),
            'groupe': ('billing.serializers.GroupeSerializer',{'many': False}),
            'rubrique_object': ('bareme.serializers.RubriqueSerializer',{'many': False}),
             }


class GroupeLigneSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = GroupeLigne
        fields = '__all__'


        expandable_fields = {
            'groupe': ('billing.serializers.GroupeSerializer',{'many': False}),
            'tc': ('app.serializers.TcSerializer',{'many': False}),
             }


class GroupeSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = Groupe
        fields = '__all__'


        expandable_fields = {
            'groupelignes': ('billing.serializers.GroupeLigneSerializer',{'many': True}),
            'ligneprestations': ('billing.serializers.LignePrestationSerializer',{'many': True}),
            'proforma': ('billing.serializers.ProformaSerializer',{'many': False}),
            'type': ('reference.serializers.TypeSerializer',{'many': False}),
             }


class ProformaSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = Proforma
        fields = '__all__'


        expandable_fields = {
            'groupes': ('billing.serializers.GroupeSerializer',{'many': True}),
            'ligneprestations': ('billing.serializers.LignePrestationSerializer',{'many': True}),
            'ligneprestationarticles': ('billing.serializers.LignePrestationArticleSerializer',{'many': True}),
            'factures': ('billing.serializers.FactureSerializer',{'many': True}),
            'gros': ('app.serializers.GrosSerializer',{'many': False}),
            'article': ('app.serializers.ArticleSerializer',{'many': False}),
             }



