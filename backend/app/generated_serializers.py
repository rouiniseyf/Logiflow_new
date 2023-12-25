from rest_framework import serializers
from .models import *
from rest_flex_fields import FlexFieldsModelSerializer
from drf_writable_nested.serializers import WritableNestedModelSerializer


class VisiteItemSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = VisiteItem
        fields = '__all__'


        expandable_fields = {
            'visite': ('app.serializers.VisiteSerializer',{'many': False}),
            'tc': ('app.serializers.TcSerializer',{'many': False}),
             }


class VisiteSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = Visite
        fields = '__all__'


        expandable_fields = {
            'visiteitems': ('app.serializers.VisiteItemSerializer',{'many': True}),
            'gros': ('app.serializers.GrosSerializer',{'many': False}),
            'article': ('app.serializers.ArticleSerializer',{'many': False}),
            'transitaire': ('reference.serializers.TransitaireSerializer',{'many': False}),
             }


class SousArticleSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = SousArticle
        fields = '__all__'


        expandable_fields = {
            'prestationoccasionnellegroupages': ('bareme.serializers.PrestationOccasionnelleGroupageSerializer',{'many': True}),
            'proformagroupages': ('billing.serializers.ProformaGroupageSerializer',{'many': True}),
            'bonsortiegroupages': ('billing.serializers.BonSortieGroupageSerializer',{'many': True}),
            'visitegroupages': ('groupage.serializers.VisiteGroupageSerializer',{'many': True}),
            'positiongroupages': ('groupage.serializers.PositionGroupageSerializer',{'many': True}),
            'tc': ('app.serializers.TcSerializer',{'many': False}),
            'client': ('reference.serializers.ClientSerializer',{'many': False}),
            'transitaire': ('reference.serializers.TransitaireSerializer',{'many': False}),
            'box': ('reference.serializers.BoxSerializer',{'many': False}),
             }


class TcSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = Tc
        fields = '__all__'


        expandable_fields = {
            'positions': ('app.serializers.PositionSerializer',{'many': True}),
            'sousarticles': ('app.serializers.SousArticleSerializer',{'many': True}),
            'visiteitems': ('app.serializers.VisiteItemSerializer',{'many': True}),
            'scelles': ('app.serializers.ScelleSerializer',{'many': True}),
            'prestationoccasionnelles': ('bareme.serializers.PrestationOccasionnelleSerializer',{'many': True}),
            'groupelignes': ('billing.serializers.GroupeLigneSerializer',{'many': True}),
            'commandes': ('billing.serializers.CommandeSerializer',{'many': True}),
            'bonsortieitems': ('billing.serializers.BonSortieItemSerializer',{'many': True}),
            'article': ('app.serializers.ArticleSerializer',{'many': False}),
            'type_tc': ('reference.serializers.TypeSerializer',{'many': False}),
            'bulletins': ('app.serializers.BulletinsEscortSerializer',{'many': False}),
            'receved_by': ('auth.serializers.UserSerializer',{'many': False}),
            'current_scelle': ('app.serializers.ScelleSerializer',{'many': False}),
             }


class BulletinsEscortSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = BulletinsEscort
        fields = '__all__'


        expandable_fields = {
            'tcs': ('app.serializers.TcSerializer',{'many': True}),
            'gros': ('app.serializers.GrosSerializer',{'many': False}),
            'charge_chargement': ('auth.serializers.UserSerializer',{'many': False}),
            'charge_reception': ('auth.serializers.UserSerializer',{'many': False}),
             }


class PositionSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'


        expandable_fields = {
            'parc': ('reference.serializers.ParcSerializer',{'many': False}),
            'zone': ('reference.serializers.ZoneSerializer',{'many': False}),
            'tc': ('app.serializers.TcSerializer',{'many': False}),
             }


class ArticleSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'


        expandable_fields = {
            'tcs': ('app.serializers.TcSerializer',{'many': True}),
            'visites': ('app.serializers.VisiteSerializer',{'many': True}),
            'proformas': ('billing.serializers.ProformaSerializer',{'many': True}),
            'boncommandes': ('billing.serializers.BonCommandeSerializer',{'many': True}),
            'proformagroupages': ('billing.serializers.ProformaGroupageSerializer',{'many': True}),
            'visitegroupages': ('groupage.serializers.VisiteGroupageSerializer',{'many': True}),
            'gros': ('app.serializers.GrosSerializer',{'many': False}),
            'client': ('reference.serializers.ClientSerializer',{'many': False}),
            'transitaire': ('reference.serializers.TransitaireSerializer',{'many': False}),
             }


class GrosSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    articles = ArticleSerializer(many=True,required=False)
    class Meta:
        model = Gros
        fields = '__all__'


        expandable_fields = {
            'articles': ('app.serializers.ArticleSerializer',{'many': True}),
            'bulletinsescorts': ('app.serializers.BulletinsEscortSerializer',{'many': True}),
            'visites': ('app.serializers.VisiteSerializer',{'many': True}),
            'proformas': ('billing.serializers.ProformaSerializer',{'many': True}),
            'proformagroupages': ('billing.serializers.ProformaGroupageSerializer',{'many': True}),
            'visitegroupages': ('groupage.serializers.VisiteGroupageSerializer',{'many': True}),
            'port_emission': ('reference.serializers.PortSerializer',{'many': False}),
            'port_reception': ('reference.serializers.PortSerializer',{'many': False}),
            'navire': ('reference.serializers.NavireSerializer',{'many': False}),
            'armateur': ('reference.serializers.ArmateurSerializer',{'many': False}),
            'consignataire': ('reference.serializers.ConsignataireSerializer',{'many': False}),
            'bareme': ('bareme.serializers.BaremeSerializer',{'many': False}),
            'regime': ('bareme.serializers.RegimeSerializer',{'many': False}),
             }


class ScelleSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    Scelle = TcSerializer(many=True,required=False)
    class Meta:
        model = Scelle
        fields = '__all__'


        expandable_fields = {
            'Scelle': ('app.serializers.TcSerializer',{'many': True}),
            'tc': ('app.serializers.TcSerializer',{'many': False}),
             }


