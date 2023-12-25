from rest_framework import serializers
from .models import *
from rest_flex_fields import FlexFieldsModelSerializer
from drf_writable_nested.serializers import WritableNestedModelSerializer


class PositionGroupageSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = PositionGroupage
        fields = '__all__'


        expandable_fields = {
            'sous_article': ('app.serializers.SousArticleSerializer',{'many': False}),
            'box': ('reference.serializers.BoxSerializer',{'many': False}),
             }


class VisiteGroupageSerializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):
    class Meta:
        model = VisiteGroupage
        fields = '__all__'


        expandable_fields = {
            'gros': ('app.serializers.GrosSerializer',{'many': False}),
            'article': ('app.serializers.ArticleSerializer',{'many': False}),
            'sous_article': ('app.serializers.SousArticleSerializer',{'many': False}),
            'transitaire': ('reference.serializers.TransitaireSerializer',{'many': False}),
             }


