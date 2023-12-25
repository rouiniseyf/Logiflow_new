from ..forms import *
from django.http import JsonResponse
from django.core import serializers
from datetime import datetime, date
from ..models import *
import json
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from reference.models import * 
from bareme.models import *
from reference.forms import * 

@login_required(login_url='login')
def post_port(request):
    if   request.method == "POST":
        form = PortForm(request.POST)
        if form.is_valid():
            instance = form.save()
            ser_instance = serializers.serialize('json', [ instance, ])
            return JsonResponse({"instance": ser_instance,}, status=200)
        else:       
            return JsonResponse({"error": form.errors,}, status=400)

    return JsonResponse({"error": ""}, status=400)

@login_required(login_url='login')
def post_navire(request):
    if   request.method == "POST":
        form = NavireForm(request.POST)
        if form.is_valid():
            instance = form.save()
            ser_instance = serializers.serialize('json', [ instance, ])
            return JsonResponse({"instance": ser_instance,}, status=200)
        else:
            return JsonResponse({"error": form.errors,}, status=400)

    return JsonResponse({"error": ""}, status=400)

@login_required(login_url='login')
def post_armateur(request):
    if   request.method == "POST":
        form = ArmateurForm(request.POST)
        if form.is_valid():
            instance = form.save()
            ser_instance = serializers.serialize('json', [ instance, ])
            return JsonResponse({"instance": ser_instance,}, status=200)
        else:
            return JsonResponse({"error": form.errors,}, status=400)

    return JsonResponse({"error": ""}, status=400)

@login_required(login_url='login')
def post_consignataire(request):
    if   request.method == "POST":
        form = ConsignataireForm(request.POST)
        if form.is_valid():
            instance = form.save()
            ser_instance = serializers.serialize('json', [ instance, ])
            return JsonResponse({"instance": ser_instance,}, status=200)
        else:
            return JsonResponse({"error": form.errors,}, status=400)

    return JsonResponse({"error": ""}, status=400)

@login_required(login_url='login')
def post_type_tc(request):
    if   request.method == "POST":
        form = TypeTcForm(request.POST)
        if form.is_valid():
            instance = form.save()
            ser_instance = serializers.serialize('json', [ instance, ])
            return JsonResponse({"instance": ser_instance,}, status=200)
        else:
            return JsonResponse({"error": form.errors,}, status=400)

    return JsonResponse({"error": ""}, status=400)
serializers

@login_required(login_url='login')
def post_class_tc(request):
    if   request.method == "POST":
        form = ClassTcForm(request.POST)
        if form.is_valid():
            instance = form.save()
            ser_instance = serializers.serialize('json', [ instance, ])
            return JsonResponse({"instance": ser_instance,}, status=200)
        else:
            return JsonResponse({"error": form.errors,}, status=400)

    return JsonResponse({"error": ""}, status=400)

@login_required(login_url='login')
def post_transitaire(request):
    if   request.method == "POST":
        form = TransitaireForm(request.POST)
        if form.is_valid():
            instance = form.save()
            ser_instance = serializers.serialize('json', [ instance, ])
            return JsonResponse({"instance": ser_instance,}, status=200)
        else:
            return JsonResponse({"error": form.errors,}, status=400)

    return JsonResponse({"error": ""}, status=400)


@login_required(login_url='login')
def post_visite(request):
    if request.method == "POST":

        instance = Visite.objects.create(
            gros= Gros.objects.get(pk=request.POST['gros']) ,
            article = Article.objects.get(pk=request.POST['article']),
            transitaire = Transitaire.objects.get(pk=request.POST['transitaire']),
            date_visite = datetime.datetime.strptime(request.POST['date_visite'],"%Y-%m-%d"),
            type_visite = request.POST['type_visite'],
            numero = request.POST['numero'],
            badge = request.POST['badge'],
            )
        ser_instance = serializers.serialize('json', [ instance, ])
        return JsonResponse({"instance": ser_instance,}, status=200)
    else: 
        return JsonResponse({"error": ""}, status=400)



@login_required(login_url='login')
def post_client(request):
    
    if   request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            instance = form.save()
            ser_instance = serializers.serialize('json', [ instance, ])
            return JsonResponse({"instance": ser_instance,}, status=200)
        else:
            return JsonResponse({"error": form.errors,}, status=400)

    return JsonResponse({"error": ""}, status=400)