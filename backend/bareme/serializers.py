from rest_framework import serializers
from .models import *
from rest_flex_fields import FlexFieldsModelSerializer
from drf_writable_nested.serializers import WritableNestedModelSerializer
from billing.serializers import *
from billing.serializers import *
from billing.serializers import *


class PrestationVisiteGroupageSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = PrestationVisiteGroupage
        fields = '__all__'


        expandable_fields = {
            'bareme': ('bareme.serializers.BaremeSerializer',{'many': False}),
             }


class PrestationGroupageSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = PrestationGroupage
        fields = '__all__'


        expandable_fields = {
            'bareme': ('bareme.serializers.BaremeSerializer',{'many': False}),
            'rubrique': ('bareme.serializers.RubriqueSerializer',{'many': False}),
             }


class BranchementSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = Branchement
        fields = '__all__'


        expandable_fields = {
            'bareme': ('bareme.serializers.BaremeSerializer',{'many': False}),
            'type_tc': ('reference.serializers.TypeSerializer',{'many': False}),
             }



class SejourSousArticleGroupageSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = SejourSousArticleGroupage
        fields = '__all__'


        expandable_fields = {
            'bareme': ('bareme.serializers.BaremeSerializer',{'many': False}),
             }


class SejourTcGroupageSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = SejourTcGroupage
        fields = '__all__'


        expandable_fields = {
            'bareme': ('bareme.serializers.BaremeSerializer',{'many': False}),
            'type_tc': ('reference.serializers.TypeSerializer',{'many': False}),
             }

class SejourSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = Sejour
        fields = '__all__'


        expandable_fields = {
            'bareme': ('bareme.serializers.BaremeSerializer',{'many': False}),
            'type_tc': ('reference.serializers.TypeSerializer',{'many': False}),
             }



class PrestationArticleSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = PrestationArticle
        fields = '__all__'


        expandable_fields = {
            'bareme': ('bareme.serializers.BaremeSerializer',{'many': False}),
            'rubrique': ('bareme.serializers.RubriqueSerializer',{'many': False}),
             }



class PrestationOccasionnelleGroupageSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = PrestationOccasionnelleGroupage
        fields = '__all__'


        expandable_fields = {
            'sous_article': ('app.serializers.SousArticleSerializer',{'many': False}),
             }



class PrestationOccasionnelleSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = PrestationOccasionnelle
        fields = '__all__'


        expandable_fields = {
            'tc': ('app.serializers.TcSerializer',{'many': False}),
             }



class PrestationSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = Prestation
        fields = '__all__'


        expandable_fields = {
            'bareme': ('bareme.serializers.BaremeSerializer',{'many': False}),
            'rubrique': ('bareme.serializers.RubriqueSerializer',{'many': False}),
            'type_tc': ('reference.serializers.TypeSerializer',{'many': False}),
             }


class RegimeSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = Regime
        fields = '__all__'


        expandable_fields = {
            'gross': ('app.serializers.GrosSerializer',{'many': True}),
            'bareme': ('bareme.serializers.BaremeSerializer',{'many': False}),
            'parc': ('reference.serializers.ParcSerializer',{'many': False}),
             }


class BaremeSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = Bareme
        fields = '__all__'



class RubriqueSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    rubrique_prestation = LignePrestationSerializer(many=True,required=False)
    rubrique_prestation_article = LignePrestationArticleSerializer(many=True,required=False)
    rubrique_commande = CommandeSerializer(many=True,required=False)
    class Meta:
        model = Rubrique
        fields = '__all__'


        expandable_fields = {
            'prestations': ('bareme.serializers.PrestationSerializer',{'many': True}),
            'prestationarticles': ('bareme.serializers.PrestationArticleSerializer',{'many': True}),
            'prestationgroupages': ('bareme.serializers.PrestationGroupageSerializer',{'many': True}),
            'rubrique_prestation': ('billing.serializers.LignePrestationSerializer',{'many': True}),
            'rubrique_prestation_article': ('billing.serializers.LignePrestationArticleSerializer',{'many': True}),
            'rubrique_commande': ('billing.serializers.CommandeSerializer',{'many': True}),
            'lignefacturelibres': ('billing.serializers.LigneFactureLibreSerializer',{'many': True}),
            'ligneproformagroupages': ('billing.serializers.LigneProformaGroupageSerializer',{'many': True}),
            'direction': ('reference.serializers.DirectionSerializer',{'many': False}),
             }


