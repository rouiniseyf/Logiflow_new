from ..models import *
from ..forms import *
from django.core.paginator import Paginator , PageNotAnInteger , EmptyPage
from django.shortcuts import render, redirect
from django.db.models import Q, Value 
from django.contrib import messages 
from django.http import JsonResponse
import json
from django.contrib.auth.models import User
from reference.models import * 
from bareme.models import *
from reference.forms import * 
from django.contrib.auth.decorators import login_required, user_passes_test

@login_required(login_url='login')
@user_passes_test(lambda u: u.groups.filter(name='FRANTOFFICE').exists(),login_url='access_denied')
def historique(request): 
    form = FilterGrosArticleForm()
    search = request.GET.get('search')
    selected_gros = request.GET.get('gros')
    selected_article = request.GET.get('article')
    data = Tc.objects.filter(article__numero=selected_article,article__gros__gros=selected_gros).values("tc",)

    gros = Gros.objects.all().values("id","gros","regime__designation")

    context = { 
        'form' : form , 
        'gros' : gros,
    }

    return render(request, 'app/pages/historique.html', context)


@login_required(login_url='login')
@user_passes_test(lambda u: u.groups.filter(name='TRANSIT').exists(),login_url='access_denied')
def frais(request): 
    form = FilterGrosArticleForm()
    selected_gros = request.GET.get('gros')
    selected_article = request.GET.get('article')

    gros = Gros.objects.filter(regime__designation="OT").values("id","gros","regime__designation")

    context = {
        'form' : form , 
        'gros' : gros,
    }

    return render(request, 'app/pages/frais.html', context)

