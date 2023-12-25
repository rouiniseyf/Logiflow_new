from ..models import *
from ..forms import *
from django.core.paginator import Paginator , PageNotAnInteger , EmptyPage
from django.shortcuts import render
from django.db.models import Q, Value , Sum
from django.contrib import messages 
from django.http import JsonResponse,HttpResponseRedirect
from django.urls import reverse
from reference.models import * 
from bareme.models import *
from reference.forms import * 
from django.contrib.auth.decorators import login_required
from src.methods import *

@login_required(login_url='login')
def article_details(request, pk):
    if request.method == 'POST' and 'tc_submit' in request.POST:
        form = TcForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Success",extra_tags="success")
            return HttpResponseRedirect(reverse("article_details",args=(pk,)))
        else :
            messages.error(request,"Container already exist", extra_tags="danger")

    if request.method == 'POST' and 'sous_article_submit' in request.POST:
     
        form = SousArticleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Success",extra_tags="success")
            return HttpResponseRedirect(reverse("article_details",args=(pk,)))

        else :
            messages.error(request,"Container already exist", extra_tags="danger")

    selected_article = Article.objects.get(id=pk)
    frais_portuaires = selected_article.get_prestations_occasionnelle().filter(rubrique="FRAIS PORTUAIRES")
    immobilisation = selected_article.get_prestations_occasionnelle().filter(rubrique="IMMOBILISATION")

    selected_tc = Tc.objects.filter(article=selected_article)
    sous_articles = []
    if selected_article.groupage: 
        for item in Tc.objects.filter(article=selected_article): 
            result = SousArticle.objects.filter(tc=item).order_by("numero")
            for item in result: 
                sous_articles.append(item)

    search = request.GET.get('search')
    form_tc = TcForm(initial={'article': selected_article})   
    form_sous_article = SousArticleForm(initial={'tc': selected_tc.first})   
    type_tc_form = TypeTcForm()
    types = Type.objects.all()
    if search != None and search != "": 
        form = SearchForm(request.GET)
        if form.is_valid(): 
            form = SearchForm(initial={'search': search})
            queryset = Tc.objects.filter(article_id=pk).filter(
                Q(tc__icontains=search) | Q(article__client__raison_sociale__icontains=search) | Q(article__transitaire__raison_sociale__icontains=search) | Q(tar__icontains=search)
                )
            context = {
                'article':selected_article,
                'sous_articles': sous_articles,
                'gros':selected_article.gros.id,
                'tcs': queryset,
                'form': form,
                "form_tc": form_tc,
                "form_sous_article": form_sous_article,
                'type_tc_form': type_tc_form, 
                'types' : types, 
                'frais_portuaires': get_sum_prix(frais_portuaires),
                'immobilisation': get_sum_prix(immobilisation)
            }
            return render(request,'app/pages/article_details.html',context)
    else:        
        form = SearchForm()
        tcs = Tc.objects.filter(article_id=selected_article).values("id","tc","tar","poids","article__client__raison_sociale","type_tc","dangereux","frigo")
        page = request.GET.get('page',1)
        if page == "all": 
            context = {
                'article':selected_article,
                'sous_articles': sous_articles,
                'gros':selected_article.gros.id,
                'tcs': tcs,
                'form': form,
                'form_tc': form_tc,
                "form_sous_article": form_sous_article,
                'type_tc_form': type_tc_form,
                'types' : types,
                'frais_portuaires': get_sum_prix(frais_portuaires),
                'immobilisation': get_sum_prix(immobilisation)
            }
            return render(request,"app/pages/article_details.html", context)
        else:   
            paginator = Paginator(tcs,10)
            try: 
                recoreds = paginator.page(page)
            except PageNotAnInteger: 
                recoreds = paginator.page(1)
            except EmptyPage : 
                recoreds = paginator.page(paginator.num_pages)
            context = {
                'article':selected_article,
                'sous_articles': sous_articles,
                'gros':selected_article.gros.id,
                'tcs': recoreds,
                'form': form,
                'form_tc': form_tc ,
                "form_sous_article": form_sous_article, 
                'type_tc_form': type_tc_form,
                'types' : types, 
                'frais_portuaires': get_sum_prix(frais_portuaires),
                'immobilisation': get_sum_prix(immobilisation)

            }
            return render(request,"app/pages/article_details.html",context)

@login_required(login_url='login')
def articles_by_gros(request):
    if request.method == "GET":

        gros = Gros.objects.get(id = int(request.GET.get("gros_id")))
        
        return JsonResponse({"data": serialize(gros.get_articles().values('id','numero')) }, status=200)
    else:
        return JsonResponse({"error": "Somthing happned",}, status=400)

def vuaquai(id): 
    tcs = Tc.objects.filter(article__id=id).filter(date_entree_port_sec__isnull = False, receved = True)
    return len(tcs) > 0 

@login_required(login_url='login')    
def articles_by_gros_visite(request):
    if request.method == "GET":
        gros = Gros.objects.get(id = int(request.GET.get("gros_id")))
        return JsonResponse({"data": serialize(gros.get_articles_with_receved_cotainers().values('id','numero')) }, status=200)
    else:
        return JsonResponse({"error": "Somthing happned",}, status=400)
    
@login_required(login_url='login')    
def articles_groupage_by_gros_visite(request):
    if request.method == "GET":
        gros = Gros.objects.get(id = int(request.GET.get("gros_id")))
        return JsonResponse({"data": serialize(gros.get_articles_with_receved_cotainers().filter(groupage=True).values('id','numero')) }, status=200)
    else:
        return JsonResponse({"error": "Somthing happned",}, status=400)