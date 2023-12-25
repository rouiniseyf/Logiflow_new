from rest_framework import serializers
from .models import *
from rest_flex_fields import FlexFieldsModelSerializer
from drf_writable_nested.serializers import WritableNestedModelSerializer
from app.serializers import *
from app.serializers import *


class DirectionSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = Direction
        fields = '__all__'


class BanqueSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = Banque
        fields = '__all__'


class ZoneSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = Zone
        fields = '__all__'


        expandable_fields = {
            'positions': ('app.serializers.PositionSerializer',{'many': True}),
            'parc': ('reference.serializers.ParcSerializer',{'many': False}),
             }


class BoxSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = Box
        fields = '__all__'


        expandable_fields = {
            'sousarticles': ('app.serializers.SousArticleSerializer',{'many': True}),
            'positiongroupages': ('groupage.serializers.PositionGroupageSerializer',{'many': True}),
            'parc': ('reference.serializers.ParcSerializer',{'many': False}),
             }


class ParcSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = Parc
        fields = '__all__'


class ClientSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


        expandable_fields = {
            'articles': ('app.serializers.ArticleSerializer',{'many': True}),
            'sousarticles': ('app.serializers.SousArticleSerializer',{'many': True}),
            'facturelibres': ('billing.serializers.FactureLibreSerializer',{'many': True}),
            'bareme': ('bareme.serializers.BaremeSerializer',{'many': False}),
             }


class AgentSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = Agent
        fields = '__all__'


class ConsignataireSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = Consignataire
        fields = '__all__'


class ArmateurSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = Armateur
        fields = '__all__'


class NavireSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = Navire
        fields = '__all__'


class GroupeurSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = Groupeur
        fields = '__all__'


class TransitaireSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = Transitaire
        fields = '__all__'


class TypeSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'


class PaysSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = Pays
        fields = '__all__'


class PortSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
   
    class Meta:
        model = Port
        fields = '__all__'


        expandable_fields = {
            'port_emission': ('app.serializers.GrosSerializer',{'many': True}),
            'port_reception': ('app.serializers.GrosSerializer',{'many': True}),
            'pays': ('reference.serializers.PaysSerializer',{'many': False}),
             }


