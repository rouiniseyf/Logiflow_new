from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.templatetags.static import static
from django.core.files.storage import default_storage
from django.contrib.auth.decorators import login_required, user_passes_test
from .authentication import *
from ..forms import *
from django.http import JsonResponse
from ..models import *
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
import json
from django.core.paginator import Paginator , PageNotAnInteger , EmptyPage
from django.contrib.postgres.search import SearchQuery
from django.db.models import Q, Value 
from django.db.models.functions import Concat  
from ..pagination import *
from .foreign_views import *
from .article_view import *
from .gros_view import *
from .tc_view import *
from .transfert_view import *
from .historique_view import *
from .visite_view import *
from reference.models import * 
from bareme.models import *
from reference.forms import * 
from django.utils import timezone
from src.methods import ratio
from billing.models import FactureGroupage, total_paiements
from decimal import Decimal
from rest_framework.response import Response
from rest_framework import viewsets,filters,status,generics
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from ..models import *
from django_filters.rest_framework import DjangoFilterBackend
from bareme.serializers import *
from reference.serializers import *
from billing.serializers import *
from reporting.serializers import *
from groupage.serializers import *
from rest_framework.permissions import AllowAny
from ..filters import *
import datetime
from rest_flex_fields import is_expanded

def client_exist(_raison_sociale): 
    exist = Client.objects.filter(raison_sociale=_raison_sociale).exists()


def extract_lines(file_name):
    result = []
    with file_name  as opend_file:
        for line in opend_file :
            stripped_line = line.strip().decode('latin1')
            stripped_line = stripped_line[:-1]
            splited_lien = stripped_line.rsplit("|")
            splited_lien = [item for item in splited_lien if item!= '']
            if len(splited_lien) > 0 :     
                splited_lien = removeImpurities(splited_lien)          
                result.append(splited_lien) 
    return result


def extract_tcs(gros, conta , ligne): 
    articles_groupage = []
    for line in ligne:
        numero_article = line[2]
        add  = True  
        if len(line[3]) > 4 : 
            BL = line[3]
            designation_marchandise = line[4]
            raison_sociale_client = line[9]
            adress_client = line[10]
            poids = line[11]
            groupage = False

        else: 
            if line[3] != 0: 
                add = False
                articles_groupage.append(line[2])
            else: 
                numero_sous_article = line[3]
                BL = line[4]
                designation_marchandise = line[5]
                raison_sociale_client = line[10]
                adress_client = line[11]
                poids = line[12] 
                groupage = True  

        try: 
            if not (client_exist(raison_sociale_client)): 
                    client= Client(raison_sociale = raison_sociale_client , adress = adress_client )
                    client.save()
        except:
            pass  
        
        if add : 
            if(Article.objects.filter(numero = numero_article, gros = gros).exists()): 
                article = Article.objects.get(numero=numero_article, gros=gros)
            else: 
                article = Article.objects.create(numero = numero_article, gros = gros ,bl=BL,groupage = groupage ,client = Client.objects.get(raison_sociale = raison_sociale_client),designation = designation_marchandise)
            
            if article.groupage : 
                pass
            else : 

                for conta_line in conta: 
                    if article.numero == conta_line[2]:
    
                        tc = conta_line[3]
                        tar = conta_line[4]

                        if(Tc.objects.filter(article=article, tc = tc).exists() == False ):
                            added_tc = Tc.objects.create(article = article,tc=tc, tar = tar, poids=poids)

    add_sous_article(gros,ligne,list(dict.fromkeys(articles_groupage)))
    #update_sous_article(gros,ligne,list(dict.fromkeys(articles_groupage)))
  
def extract_tcs_update_sous_articles(gros, conta , ligne): 
    articles_groupage = []
    for line in ligne:
        numero_article = line[2]
        add  = True  
        if len(line[3]) > 4 : 
            BL = line[3]
            designation_marchandise = line[4]
            raison_sociale_client = line[9]
            adress_client = line[10]
            poids = line[11]
            groupage = False

        else: 
            if line[3] != 0: 
                add = False
                articles_groupage.append(line[2])
            else: 
                numero_sous_article = line[3]
                BL = line[4]
                designation_marchandise = line[5]
                raison_sociale_client = line[10]
                adress_client = line[11]
                poids = line[12] 
                groupage = True  

        try: 
            if not (client_exist(raison_sociale_client)): 
                    client= Client(raison_sociale = raison_sociale_client , adress = adress_client )
                    client.save()
        except:
            pass  
        
        if add : 
            if(Article.objects.filter(numero = numero_article, gros = gros).exists()): 
                article = Article.objects.get(numero=numero_article, gros=gros)
            else: 
                article = Article.objects.create(numero = numero_article, gros = gros ,bl=BL,groupage = groupage ,client = Client.objects.get(raison_sociale = raison_sociale_client),designation = designation_marchandise)
            
            if article.groupage : 
                pass
            else : 

                for conta_line in conta: 
                    if article.numero == conta_line[2]:

                        tc = conta_line[3]
                        tar = conta_line[4]

                        if(not Tc.objects.filter(article=article, tc = tc).exists() ):
                            Tc.objects.filter(article = article,tc=tc)

    add_sous_article(gros,ligne,list(dict.fromkeys(articles_groupage)))

def add_sous_article(gros,ligne, groupage_list):   

    for article in groupage_list: 
        gros.article_set.filter(numero = article).update(groupage = True)
        current_article = gros.article_set.get(numero = article)


        tc = current_article.tc_set.all().first()   
  
        for line in ligne:
            if ( line[2] == article ) & ( len(line[3]) < 4 ) :  
                raison_sociale_client = line[10]
                adress_client = line[11]
                print("Sous Article: "+line[3] + "Description: "+line[5])
                try: 
                    if not (client_exist(raison_sociale_client)): 
                            client= Client(raison_sociale = raison_sociale_client , adress = adress_client)
                            client.save()
                except:
                    pass            
                poids = line[12].replace(',','.')
                if not SousArticle.objects.filter(tc = tc,numero = line[3]).exists():
                    SousArticle.objects.create(tc = tc,numero = line[3],nombre_colis = line[7] , poids = poids , client = Client.objects.get(raison_sociale = raison_sociale_client),designation = line[5])

@login_required(login_url='login')
def chargement_sous_articles(request,pk):
    if request.method == 'POST':
        instance = Gros.objects.get(id=pk)
        conta_file = request.FILES['conta']
        ligne_file = request.FILES['ligne']  
        conta_lines = extract_lines(conta_file)
        ligne_lines = extract_lines(ligne_file)
        extract_tcs(instance,conta_lines, ligne_lines)
        extract_tcs_update_sous_articles(instance,conta_lines, ligne_lines)
        return redirect('groupage_gros_details', pk=pk)



def update_sous_article(gros,ligne, groupage_list): 
    for article in groupage_list: 
        gros.article_set.filter(numero = article).update(groupage = True)
        current_article = gros.article_set.get(numero = article)
        tc = current_article.tc_set.all().first()        
        for line in ligne:
            if ( line[2] == article ) & ( len(line[3]) < 4 ) :        
                
                SousArticle.objects.filter(tc = tc,numero = line[3]).update(nombre_colis = line[7])
                            
def get_articles_tcs(gros): 
    articles = gros.article_set.all()
    i = 0
    while i < len(articles):
        articles[i].tcs = Tc.objects.filter(article_id=articles[i].id)
        i = i + 1


def remove(string):
    return "".join(string.split())


def removeImpurities(array): 
    array.pop()
    new_array = []
    for item in array: 
        if remove(item) != "0" and remove(item) != "00" and remove(item) != "000" and remove(item) != "0000"  : 
            new_array.append(item)
    return new_array

@login_required(login_url='login')
def chargement_gros(request,pk):
    if request.method == 'POST':
        instance = Gros.objects.get(id=pk)
        conta_file = request.FILES['conta']
        ligne_file = request.FILES['ligne']  
        conta_lines = extract_lines(conta_file)
        ligne_lines = extract_lines(ligne_file)
        extract_tcs(instance,conta_lines, ligne_lines)
        articles = Article.objects.filter(gros_id=instance.id)
        i = 0
        while i < len(articles):
            articles[i].tcs = Tc.objects.filter(article_id=articles[i].id)
            i = i + 1
            
        return render(request,"app/pages/gros_details.html", {"gros":instance, "articles": articles})

def test(request): 

    return render(request,'app/pages/dashboard2.html')

from datetime import datetime, timedelta
from django import template
from django.contrib.auth.decorators import login_required

register = template.Library()

@register.filter(name='has_group')
@login_required(login_url='login')
def dashboard(request):
    # Current day, week, month, year & last week -----------
    today = datetime.now()

    yesterday = (today - timedelta(days=1)).date()

    start_of_this_week = today - timedelta(days=today.weekday())
    start_of_this_week = start_of_this_week.date()

    if today.strftime("%A", locale='fr') == "samedi":
        first_day_of_this_week = today.date()
        first_day_of_last_week = (today - timedelta(weeks=1)).date()
        first_day_this_week = today.strftime('%-d', locale='fr')
    else:
        first_day_of_this_week = today - timedelta(days=(today.weekday() + 1) % 7)
        first_day_of_this_week = first_day_of_this_week.date()
        first_day_of_last_week = (today - timedelta(days=(today.weekday() + 1) % 7, weeks=1)).date()
        first_day_this_week = first_day_of_this_week.strftime('%-d', locale='fr')

    if today.strftime("%A", locale='fr') == "vendredi":
        last_day_of_this_week = today.date()
        last_day_of_last_week = (today - timedelta(weeks=1)).date()
        last_day_this_week = today.strftime('%-d', locale='fr')
    else:
        last_day_of_this_week = today + timedelta(days=(4 - today.weekday()) % 7)
        last_day_of_this_week = last_day_of_this_week.date()
        last_day_of_last_week = (today + timedelta(days=(4 - today.weekday()) % 7, weeks=1)).date()
        last_day_this_week = last_day_of_this_week.strftime('%-d', locale='fr')

    # Continue with the rest of your code...

    return render(request, 'your_template.html', context)


    first_day_of_this_month = today.start_of('month').to_date_string()
    last_day_of_this_month = today.end_of('month').to_date_string()

    first_day_of_this_year = today.start_of('year').to_date_string()
    last_day_of_this_year = today.end_of('year').to_date_string()

    # Last month --------------
    last_month = today.start_of('month').subtract(months=1)
    first_day_of_last_month = last_month.start_of('month').to_date_string()
    last_day_of_last_month = last_month.end_of('month').to_date_string()

    this_month = today.start_of('month')
    # Last year -------------- 
    last_year = today.subtract(years=1)


    first_day_of_last_year = last_year.start_of("year").to_date_string()
    last_day_od_last_year = last_year.end_of("year").to_date_string()

    #Today ---------
    today = today.to_date_string()

    total_today = total_paiements(today,today)
    total_this_week = total_paiements(first_day_of_this_week,last_day_of_this_week)
    total_this_month= total_paiements(first_day_of_this_month,last_day_of_this_month)
    total_this_year= total_paiements(first_day_of_this_year,last_day_of_this_year)

    total_yesterday = total_paiements(yesterday,yesterday)
  
    
    total_last_week = total_paiements(first_day_of_last_week,last_day_of_last_week)
    total_last_month = total_paiements(first_day_of_last_month,last_day_of_last_month)
    total_last_year = total_paiements(first_day_of_last_year,last_day_od_last_year)

    
    ratio_day = ratio(total_yesterday,total_today)
    ratio_week = ratio(total_last_week,total_this_week)
    ratio_month = ratio(total_last_month,total_this_month)
    ratio_year = ratio(total_last_year,total_this_year)

    this_month = this_month.format('MMM', locale='fr')
    last_month = last_month.format('MMM', locale='fr')


    this_year = pendulum.now().format('Y', locale='fr')
    last_year = last_year.format('Y', locale='fr')

    processed_invoices_this_year = len(Facture.objects.filter(date_creation__range=[first_day_of_this_year,last_day_of_this_year]))
    processed_comolimentary_invoices_this_year = len(FactureComplementaire.objects.filter(date_creation__range=[first_day_of_this_year,last_day_of_this_year]))
    processed_free_invoices_this_year = len(FactureLibre.objects.filter(date_creation__range=[first_day_of_this_year,last_day_of_this_year]))
    processed_groupage_invoices_this_year = len(FactureGroupage.objects.filter(date_creation__range=[first_day_of_this_year,last_day_of_this_year]))

    processed_invoices_this_month = len(Facture.objects.filter(date_creation__range=[first_day_of_this_month,last_day_of_this_month]))
    processed_comolimentary_invoices_this_month = len(FactureComplementaire.objects.filter(date_creation__range=[first_day_of_this_month,last_day_of_this_month]))
    processed_free_invoices_this_month = len(FactureLibre.objects.filter(date_creation__range=[first_day_of_this_month,last_day_of_this_month]))
    processed_groupage_invoices_this_month = len(FactureGroupage.objects.filter(date_creation__range=[first_day_of_this_month,last_day_of_this_month]))

    processed_invoices_this_week = len(Facture.objects.filter(date_creation__range=[first_day_of_last_week,last_day_of_last_week]))
    processed_comolimentary_invoices_this_week = len(FactureComplementaire.objects.filter(date_creation__range=[first_day_of_last_week,last_day_of_last_week]))
    processed_free_invoices_this_week = len(FactureLibre.objects.filter(date_creation__range=[first_day_of_last_week,last_day_of_last_week]))
    processed_groupage_invoices_this_week = len(FactureGroupage.objects.filter(date_creation__range=[first_day_of_last_week,last_day_of_last_week]))
    
    processed_invoices_today = len(Facture.objects.filter(date_creation=today))
    processed_comolimentary_invoices_today = len(FactureComplementaire.objects.filter(date_creation=today))
    processed_free_invoices_today = len(FactureLibre.objects.filter(date_creation=today))
    processed_groupage_invoices_today = len(FactureGroupage.objects.filter(date_creation=today))
    
       
    total_processed_files_this_year = processed_invoices_this_year + processed_comolimentary_invoices_this_year + processed_free_invoices_this_year + processed_groupage_invoices_this_year
    total_processed_files_this_month = processed_invoices_this_month + processed_comolimentary_invoices_this_month + processed_free_invoices_this_month + processed_groupage_invoices_this_month
    total_processed_files_this_week = processed_invoices_this_week + processed_comolimentary_invoices_this_week + processed_free_invoices_this_week + processed_groupage_invoices_this_week
    total_processed_files_today = processed_invoices_today + processed_comolimentary_invoices_today + processed_free_invoices_today + processed_groupage_invoices_today
    
    got_in_this_year = len(Tc.objects.filter(date_entree_port_sec__range = [first_day_of_this_year,last_day_of_this_year]))
    got_in_this_month= len(Tc.objects.filter(date_entree_port_sec__range = [first_day_of_this_month,last_day_of_this_month]))
    got_in_this_week= len(Tc.objects.filter(date_entree_port_sec__range = [first_day_of_this_week,last_day_of_this_week]))
    got_in_today= len(Tc.objects.filter(date_entree_port_sec = today))


    
    if len(request.user.groups.all()) > 0 and len(request.user.groups.all()) < 2 : 
        groupe = request.user.groups.all().first()
        if groupe.name == "POINTEUR":
            return redirect('update_position')
        elif groupe.name == "TRANSIT":
            return redirect('gros_view')
        else: 
            gros_count_year = Gros.objects.all().count()
            tc_count = Tc.objects.all().count()
            context = {
                "text" : "this is just a test",
                "gros_count_year" : gros_count_year, 
                "tc_count" : tc_count,
                'this_year': this_year,
                'last_year': last_year, 
                'this_month': this_month.capitalize(), 
                'last_month': last_month, 
                'ratio_day':ratio_day ,
                'ratio_week':ratio_week, 
                'ratio_month': ratio_month, 
                'ratio_year': ratio_year,
                'first_day_this_week':first_day_this_week,
                'last_day_this_week':last_day_this_week ,
                'today' : pendulum.now().format('YYYY-MM-DD'),
                'total_this_day' : total_today,
                'total_this_year' : total_this_year,
                'total_last_year' : total_last_year,
                'total_this_month' : total_this_month,
                'total_last_month' : total_last_month,
                'total_this_week' : total_this_week,
                'total_last_week' : total_last_week,
                'total_processed_files_this_year': total_processed_files_this_year,
                'total_processed_files_this_month': total_processed_files_this_month,
                'total_processed_files_this_week': total_processed_files_this_week,
                'total_processed_files_today': total_processed_files_today,
                'got_in_this_year' : got_in_this_year,
                'got_in_this_month': got_in_this_month,
                'got_in_this_week': got_in_this_week,
                'got_in_today': got_in_today,
            }
            return render(request, 'app/pages/dashboard.html', context)
    else: 
        today = datetime.datetime.now()
        gros_count_year = Gros.objects.filter(accostage__year = today.year).count()
        gros_count_month = Gros.objects.filter(accostage__month = today.month).count()
        tc_count_year = Tc.objects.filter(date_entree_port_sec__year=today.year).count()
        tc_count_month = Tc.objects.filter(date_entree_port_sec__month=today.month).count()
        tc_count_today = Tc.objects.filter(date_entree_port_sec__day = today.day).count()
        parcs = Parc.objects.all()

        without_duplicates = [] 
        positions = Position.objects.filter(tc__billed=False)
        for position in positions : 
            exists = False 
            for item in without_duplicates : 
                if item.tc == position.tc : 
                    exists = True 
            if not exists : 
                without_duplicates.append(position)
   
        without_duplicates_updated = []
        for item in without_duplicates : 
            exists = False 
            for elem in without_duplicates_updated : 
                if elem.tc == item.tc: 
                    exits = True 
            if not exists :         
                position = Position.objects.filter(tc= item.tc).order_by("date_position").last()
                without_duplicates_updated.append(position)

        percs_info = []

        for item in without_duplicates_updated: 
            exits = False
            for parc in percs_info : 
                if item.parc == parc["parc"] : 
                    exits = True 
                    parc["tcs"].append(item.tc) 
            
            if not exits : 
                percs_info.append({
                    "parc" : item.parc, 
                    "tcs" : [item.tc,]
                })


        for parc_info in percs_info :
            
            types = []
            for item in parc_info["tcs"] : 
                exists = False 
                for type in types :
                    if item.type_tc == type["type"] and type["dangereux"] == item.dangereux and type["frigo"] == item.frigo : 
                        exists = True 
                        type["tcs"].append(elem.tc)  
     
                if not exists: 
                
                    types.append(
                        {
                            "type" : item.type_tc , 
                            "dangereux" : item.dangereux , 
                            "frigo" : item.frigo , 
                            "tcs" : [item],
                        }
                    )

            parc_info["types"] = types       


        for item in percs_info : 
            for elem in item["types"] : 
                elem["count"] = len(elem["tcs"])

  
        context = {
            "gros_count_year" : gros_count_year, 
            "gros_count_month" : gros_count_month, 
            "tc_count_year" : tc_count_year,
            "tc_count_month" : tc_count_month,
            "tc_count_today" : tc_count_today,
            "parcs" : parcs,
            "percs_info": percs_info,
            'this_year': this_year,
            'last_year': last_year, 
            'this_month': this_month.capitalize(), 
            'last_month': last_month, 
            'ratio_day':ratio_day ,
            'ratio_week':ratio_week, 
            'ratio_month': ratio_month, 
            'ratio_year': ratio_year,
            'first_day_this_week':first_day_this_week,
            'last_day_this_week':last_day_this_week ,
            'today' : pendulum.now().format('YYYY-MM-DD'),
            'total_this_day' : total_today,
            'total_yesterday' : total_yesterday,
            'total_this_year' : total_this_year,
            'total_last_year' : total_last_year,
            'total_this_month' : total_this_month,
            'total_last_month' : total_last_month,
            'total_this_week' : total_this_week,
            'total_last_week' : total_last_week,
            'total_processed_files_this_year': total_processed_files_this_year,
            'total_processed_files_this_month': total_processed_files_this_month,
            'total_processed_files_this_week': total_processed_files_this_week,
            'total_processed_files_today': total_processed_files_today,
            'got_in_this_year' : got_in_this_year,
            'got_in_this_month': got_in_this_month,
            'got_in_this_week': got_in_this_week,
            'got_in_today': got_in_today,
        }
        return render(request, 'app/pages/dashboard.html',context)


def access_denied(request): 

    return  render(request, 'app/pages/access_denied.html')


def get_tc_and_articles(selected_gros): 
    articles = Article.objects.filter(gros_id=selected_gros.id)
    i = 0
    while i < len(articles):
        articles[i].tcs = Tc.objects.filter(article_id=articles[i].id)
        i += 1
    return articles



@login_required(login_url='login')
@user_passes_test(lambda u: u.groups.filter(name='TRANSIT').exists(),login_url='access_denied')
def saisie_manuelle(request, pk): 
    selected_gros = Gros.objects.get(id=pk)

    context = {
        'gros' : selected_gros,
    }
    return render(request,'app/pages/saisie_manuelle.html', context)

@login_required(login_url='login')
@csrf_exempt
def get_port_id(request):
	if request.is_ajax():
		nom = request.GET['raison_sociale']
		port_id = Port.objects.get(raison_sociale = nom).id
		data = {'port_id':port_id,}
		return HttpResponse(json.dumps(data), content_type='application/json')
	return HttpResponse("/")

@login_required(login_url='login')
def get_tcs_by_gros(request):
    if   request.method == "GET":
        selected_gros_id = request.GET.get("id")
        page = int(request.GET.get("page"))

        all_records = Tc.objects.filter(article__gros__id=selected_gros_id).values(
            "id",
            "article_id",
            "article",
            "tc",
            "tar",
            "poids",
            "article__client__id",
            "article__client__raison_sociale",
            "article__transitaire__id",
            "article__transitaire__raison_sociale",
            )
        
        [records, pagination] = paginate(all_records, 15, page)
        serialized_records = []
        for record in records : 
            serialized_records.append(record)
        return JsonResponse({"data": serialized_records,"pagination":pagination }, status=200)

    else:
        return JsonResponse({"error": "Somthing happned",}, status=400)

    return JsonResponse({"error": ""}, status=400)


@login_required(login_url='login')
def get_gros(request):
    page = int(request.GET.get("page"))

    if   request.method == "GET":
        all_records = Gros.objects.all().values(
            "id",
            "numero",
            "accostage",
            "tc",
            "tar",
            "poids",
            "article__client__id",
            "article__client__raison_sociale",
            "article__transitaire__id",
            "article__transitaire__raison_sociale",
            )
        
        [records, pagination] = paginate(all_records, 15, page)
        serialized_records = []
        for record in records : 
            serialized_records.append(record)

        return JsonResponse({"data": serialized_records,"pagination":pagination }, status=200)

    else:
        return JsonResponse({"error": "Somthing happned",}, status=400)



def super_admin(request): 
    
    _regime = Regime.objects.get(designation = "D1")
    gros_with_not_recived_containers = [gros for gros in Gros.objects.filter(regime = _regime) if gros.has_articles_with_not_receved_containers]
    
    context = {
        'data' : gros_with_not_recived_containers,
    }
    return render(request,'app/pages/super_admin.html',context)

def etats(request): 
    
    context = {
    }
    return render(request,'app/pages/etats.html',context)

def receive(request): 
  
    if request.method == "POST":
        selected_gros_id = request.POST.get("id")

        Tc.objects.filter(article__gros__id = selected_gros_id, date_entree_port_sec__isnull = True).update(date_entree_port_sec = pendulum.today(), receved = True)
    
    return JsonResponse({"message": 'success'}, status=200)

    

@login_required(login_url='login')
def etat_de_case(request):

    date1 = request.POST.get('depuis')
    date2 = request.POST.get('jusqua')
    numero = request.POST.get('numero')
    if date1 > date2 : 
        jusqua = date1 
        depuis = date2 
    else: 
        jusqua = date2 
        depuis = date1 

    # paiements = Paiement.objects.filter(date__gte=depuis,date__lte=jusqua)
    # paiements_groupage = PaiementGroupage.objects.filter(date__gte=depuis,date__lte=jusqua)

    factures = Facture.objects.filter(proforma__date_proforma__gte=depuis,proforma__date_proforma__lte=jusqua)
    factures_groupage = FactureGroupage.objects.filter(proforma__date_proforma__gte=depuis,proforma__date_proforma__lte=jusqua)
    results = []
    for facture in factures: 
        results.append({"facture": facture, "paiamants": facture.get_paiements()})
    for facture in factures_groupage: 
        results.append({"facture": facture, "paiamants": facture.get_paiements()})  


    context = {
        "date1": date1, 
        "date2": date2,
        "numero": numero,
        "results": results
    }  

    pdf = render_to_pdf('app/reporting/etat_de_case.html', context)
    return HttpResponse(pdf, content_type='application/pdf')



@csrf_exempt
def vu_a_qaui(request):
	
    gros = request.GET['gros']
    article = request.GET['article']
    vu = Article.objects.get(gros__numero = gros, numero = article).has_receved_containers
    data = {'vu':vu,}
    return HttpResponse(json.dumps(data), content_type='application/json')
	#return HttpResponse("/")


#---------------------------------

class TcList(generics.ListAPIView,generics.GenericAPIView): 

    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['tc',] 
    # filterset_class= TcFilter
    # permission_classes = [AllowAny]
    queryset = Tc.objects.all().order_by("-id")  
    serializer_class = TcSerializer 

    # ordering_fields = ['date',  ]

    def get(self, request, *args, **kwargs): 
        return self.list(request, *args, **kwargs)



class GrosList(generics.ListAPIView,generics.GenericAPIView): 

    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['designation','id',] 
    permission_classes = [AllowAny]
    queryset = Gros.objects.all().order_by("-id")  
    serializer_class = GrosSerializer 
    filterset_class= GrosFilter


    # ordering_fields = ['date',  ]

    def get(self, request, *args, **kwargs): 
        return self.list(request, *args, **kwargs)


class ArticleList(generics.ListAPIView,generics.GenericAPIView): 

    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    permission_classes = [AllowAny]
    queryset = Article.objects.all().order_by("-id")  
    serializer_class = ArticleSerializer 
    filterset_class= ArticleFilter


    # ordering_fields = ['date',  ]

    def get(self, request, *args, **kwargs): 
        return self.list(request, *args, **kwargs)

#-------------------------------------------------- 


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000


class GrosViewSet(viewsets.ModelViewSet):
    queryset = Gros.objects.all()
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    serializer_class = GrosSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    filterset_class= GrosFilter
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()


        # Update nested port_emission
        port_emission_data = request.data.pop('port_emission', None)
        if isinstance(port_emission_data, int):
            request.data['port_emission'] = port_emission_data
        elif port_emission_data:
            port_emission_id = port_emission_data.get('id')
            if port_emission_id:
                # If 'id' is present, it's an update
                port_emission_instance = Port.objects.get(id=port_emission_id)
                port_emission_serializer = PortSerializer(port_emission_instance,data=port_emission_data, partial=partial)
                port_emission_serializer.is_valid(raise_exception=True)
                port_emission_serializer.save()
            else:
                # If 'id' is not present, it's a create
                port_emission_serializer = PortSerializer(data=port_emission_data)
                port_emission_serializer.is_valid(raise_exception=True)
                port_emission = port_emission_serializer.save()
                request.data['port_emission'] = port_emission.id


        # Update nested port_reception
        port_reception_data = request.data.pop('port_reception', None)
        if isinstance(port_reception_data, int):
            request.data['port_reception'] = port_reception_data
        elif port_reception_data:
            port_reception_id = port_reception_data.get('id')
            if port_reception_id:
                # If 'id' is present, it's an update
                port_reception_instance = Port.objects.get(id=port_reception_id)
                port_reception_serializer = PortSerializer(port_reception_instance,data=port_reception_data, partial=partial)
                port_reception_serializer.is_valid(raise_exception=True)
                port_reception_serializer.save()
            else:
                # If 'id' is not present, it's a create
                port_reception_serializer = PortSerializer(data=port_reception_data)
                port_reception_serializer.is_valid(raise_exception=True)
                port_reception = port_reception_serializer.save()
                request.data['port_reception'] = port_reception.id


        # Update nested navire
        navire_data = request.data.pop('navire', None)
        if isinstance(navire_data, int):
            request.data['navire'] = navire_data
        elif navire_data:
            navire_id = navire_data.get('id')
            if navire_id:
                # If 'id' is present, it's an update
                navire_instance = Navire.objects.get(id=navire_id)
                navire_serializer = NavireSerializer(navire_instance,data=navire_data, partial=partial)
                navire_serializer.is_valid(raise_exception=True)
                navire_serializer.save()
            else:
                # If 'id' is not present, it's a create
                navire_serializer = NavireSerializer(data=navire_data)
                navire_serializer.is_valid(raise_exception=True)
                navire = navire_serializer.save()
                request.data['navire'] = navire.id


        # Update nested armateur
        armateur_data = request.data.pop('armateur', None)
        if isinstance(armateur_data, int):
            request.data['armateur'] = armateur_data
        elif armateur_data:
            armateur_id = armateur_data.get('id')
            if armateur_id:
                # If 'id' is present, it's an update
                armateur_instance = Armateur.objects.get(id=armateur_id)
                armateur_serializer = ArmateurSerializer(armateur_instance,data=armateur_data, partial=partial)
                armateur_serializer.is_valid(raise_exception=True)
                armateur_serializer.save()
            else:
                # If 'id' is not present, it's a create
                armateur_serializer = ArmateurSerializer(data=armateur_data)
                armateur_serializer.is_valid(raise_exception=True)
                armateur = armateur_serializer.save()
                request.data['armateur'] = armateur.id


        # Update nested consignataire
        consignataire_data = request.data.pop('consignataire', None)
        if isinstance(consignataire_data, int):
            request.data['consignataire'] = consignataire_data
        elif consignataire_data:
            consignataire_id = consignataire_data.get('id')
            if consignataire_id:
                # If 'id' is present, it's an update
                consignataire_instance = Consignataire.objects.get(id=consignataire_id)
                consignataire_serializer = ConsignataireSerializer(consignataire_instance,data=consignataire_data, partial=partial)
                consignataire_serializer.is_valid(raise_exception=True)
                consignataire_serializer.save()
            else:
                # If 'id' is not present, it's a create
                consignataire_serializer = ConsignataireSerializer(data=consignataire_data)
                consignataire_serializer.is_valid(raise_exception=True)
                consignataire = consignataire_serializer.save()
                request.data['consignataire'] = consignataire.id


        # Update nested bareme
        bareme_data = request.data.pop('bareme', None)
        if isinstance(bareme_data, int):
            request.data['bareme'] = bareme_data
        elif bareme_data:
            bareme_id = bareme_data.get('id')
            if bareme_id:
                # If 'id' is present, it's an update
                bareme_instance = Bareme.objects.get(id=bareme_id)
                bareme_serializer = BaremeSerializer(bareme_instance,data=bareme_data, partial=partial)
                bareme_serializer.is_valid(raise_exception=True)
                bareme_serializer.save()
            else:
                # If 'id' is not present, it's a create
                bareme_serializer = BaremeSerializer(data=bareme_data)
                bareme_serializer.is_valid(raise_exception=True)
                bareme = bareme_serializer.save()
                request.data['bareme'] = bareme.id


        # Update nested regime
        regime_data = request.data.pop('regime', None)
        if isinstance(regime_data, int):
            request.data['regime'] = regime_data
        elif regime_data:
            regime_id = regime_data.get('id')
            if regime_id:
                # If 'id' is present, it's an update
                regime_instance = Regime.objects.get(id=regime_id)
                regime_serializer = RegimeSerializer(regime_instance,data=regime_data, partial=partial)
                regime_serializer.is_valid(raise_exception=True)
                regime_serializer.save()
            else:
                # If 'id' is not present, it's a create
                regime_serializer = RegimeSerializer(data=regime_data)
                regime_serializer.is_valid(raise_exception=True)
                regime = regime_serializer.save()
                request.data['regime'] = regime.id


        gros_serializer = self.get_serializer(instance,data=request.data, partial=partial)
        gros_serializer.is_valid(raise_exception=True)
        gros_instance = gros_serializer.save()


        # Update nested articles 
        articles_data = request.data.pop('articles', [])
        if articles_data:
            for article_data in articles_data:
                if isinstance(article_data, int):
                    pass
                else: 
                    article_id = articles_data.get('id')
                    if article_id:
                        # If 'id' is present, it's an update
                        articles_instance = Article.objects.get(id=article_id)
                        articles_serializer = ArticleSerializer(articles_instance, data=articles_data, partial=partial)
                    else:
                        # If 'id' is not present, it's a create
                        articles_data['gros'] = gros_instance.id
                        articles_serializer = ArticleSerializer(data=articles_data)
                    articles_serializer.is_valid(raise_exception=True)
                    articles_serializer.save()
        return Response(gros_serializer.data)

    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()

    #     regime_data = request.data.pop('regime', None)
    #     if isinstance(regime_data, int):
    #         request.data["regime"] = regime_data 
    #     elif regime_data:
    #         regime_id = regime_data.get('id')
    #         if regime_id:
    #             # If 'id' is present, it's an update
    #             regime_instance = Regime.objects.get(id=regime_id)
    #             regime_serializer = RegimeSerializer(regime_instance, data=regime_data, partial=partial)
    #             regime_serializer.is_valid(raise_exception=True)
    #             regime_serializer.save()
    #         else:
    #             # If 'id' is not present, it's a create
    #             regime_serializer = RegimeSerializer(data=regime_data)
    #             regime_serializer.is_valid(raise_exception=True)
    #             regime = regime_serializer.save()
    #             request.data["regime"] = regime.id 


    #     gros_serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     gros_serializer.is_valid(raise_exception=True)
    #     gros_instance = gros_serializer.save()

    #     # Your update logic for the nested objects (articles) goes here
    #     articles_data = request.data.pop('articles', [])
    #     if articles_data: 
    #         for article_data in articles_data:
             
    #             if isinstance(article_data, int):
    #                 pass 
    #             else: 
    #                 article_id = article_data.get('id')
    #                 if article_id:
    #                     # If 'id' is present, it's an update
    #                     article_instance = Article.objects.get(id=article_id)
    #                     article_serializer = ArticleSerializer(article_instance, data=article_data, partial=partial)
    #                 else:
    #                     # If 'id' is not present, it's a create
    #                     article_data['gros'] = gros_instance.id
    #                     article_serializer = ArticleSerializer(data=article_data)

    #                 article_serializer.is_valid(raise_exception=True)
    #                 article_serializer.save()

    #     return Response(gros_serializer.data)
    
    def create(self, request, *args, **kwargs):
        articles_data = request.data.pop('articles',[])
        #| port_emission |----------------------------
        port_emission_data = request.data.get('port_emission')
        if isinstance(port_emission_data, int):
            request.data['port_emission'] = port_emission_data
        elif port_emission_data:
            port_emission_serializer = PortSerializer(data=port_emission_data)
            if port_emission_serializer.is_valid():
                port_emission = port_emission_serializer.save()
                request.data['port_emission'] = port_emission.id
            else:
                return Response(port_emission_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        #| port_reception |----------------------------
        port_reception_data = request.data.get('port_reception')
        if isinstance(port_reception_data, int):
            request.data['port_reception'] = port_reception_data
        elif port_reception_data:
            port_reception_serializer = PortSerializer(data=port_reception_data)
            if port_reception_serializer.is_valid():
                port_reception = port_reception_serializer.save()
                request.data['port_reception'] = port_reception.id
            else:
                return Response(port_reception_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        #| navire |----------------------------
        navire_data = request.data.get('navire')
        if isinstance(navire_data, int):
            request.data['navire'] = navire_data
        elif navire_data:
            navire_serializer = NavireSerializer(data=navire_data)
            if navire_serializer.is_valid():
                navire = navire_serializer.save()
                request.data['navire'] = navire.id
            else:
                return Response(navire_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        #| armateur |----------------------------
        armateur_data = request.data.get('armateur')
        if isinstance(armateur_data, int):
            request.data['armateur'] = armateur_data
        elif armateur_data:
            armateur_serializer = ArmateurSerializer(data=armateur_data)
            if armateur_serializer.is_valid():
                armateur = armateur_serializer.save()
                request.data['armateur'] = armateur.id
            else:
                return Response(armateur_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        #| consignataire |----------------------------
        consignataire_data = request.data.get('consignataire')
        if isinstance(consignataire_data, int):
            request.data['consignataire'] = consignataire_data
        elif consignataire_data:
            consignataire_serializer = ConsignataireSerializer(data=consignataire_data)
            if consignataire_serializer.is_valid():
                consignataire = consignataire_serializer.save()
                request.data['consignataire'] = consignataire.id
            else:
                return Response(consignataire_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        #| bareme |----------------------------
        bareme_data = request.data.get('bareme')
        if isinstance(bareme_data, int):
            request.data['bareme'] = bareme_data
        elif bareme_data:
            bareme_serializer = BaremeSerializer(data=bareme_data)
            if bareme_serializer.is_valid():
                bareme = bareme_serializer.save()
                request.data['bareme'] = bareme.id
            else:
                return Response(bareme_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        #| regime |----------------------------
        regime_data = request.data.get('regime')
        if isinstance(regime_data, int):
            request.data['regime'] = regime_data
        elif regime_data:
            regime_serializer = RegimeSerializer(data=regime_data)
            if regime_serializer.is_valid():
                regime = regime_serializer.save()
                request.data['regime'] = regime.id
            else:
                return Response(regime_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        gros_serializer = self.get_serializer(data=request.data)
        gros_serializer.is_valid(raise_exception=True)
        gros_instance = gros_serializer.save()


        #| articles |----------------------------


        for article_data in articles_data:
            article_data['gros'] = gros_instance.id
            article_serializer = ArticleSerializer(data=article_data)
            article_serializer.is_valid(raise_exception=True)
            article_serializer.save()


        headers = self.get_success_headers(gros_serializer.data)
        return Response(gros_serializer.data, status=201, headers=headers)

    def get_queryset(self):
        queryset = Gros.objects.all()
        if is_expanded(self.request, 'port_emission'):
            queryset = queryset.prefetch_related('port_emission')
        if is_expanded(self.request, 'port_reception'):
            queryset = queryset.prefetch_related('port_reception')
        if is_expanded(self.request, 'navire'):
            queryset = queryset.prefetch_related('navire')
        if is_expanded(self.request, 'armateur'):
            queryset = queryset.prefetch_related('armateur')
        if is_expanded(self.request, 'consignataire'):
            queryset = queryset.prefetch_related('consignataire')
        if is_expanded(self.request, 'bareme'):
            queryset = queryset.prefetch_related('bareme')
        if is_expanded(self.request, 'regime'):
            queryset = queryset.prefetch_related('regime')
        return queryset

        
    def list(self, request, *args, **kwargs):
        # Check if the 'all' parameter is present in the request query parameters
        if request.query_params.get('all', False):
            # If 'all' is present, return all records without pagination
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        # If 'all' is not present, proceed with pagination as usual
        return super().list(request, *args, **kwargs)


    @action(detail=False, methods=['post'])
    def bulk_delete(self, request, *args, **kwargs):
        ids = request.data.get('ids', [])
        if not ids:
           return Response({'detail': 'No IDs provided for deletion.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
           queryset = self.filter_queryset(self.get_queryset())
           deleted, _ = queryset.filter(pk__in=ids).delete()
           if deleted > 0:
               return Response({'detail': f'Successfully deleted objects with ids: {ids} .'}, status=status.HTTP_204_NO_CONTENT)
           else:
               return Response({'detail': 'No objects found for deletion.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
           return Response({'detail': f'Error during deletion: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    serializer_class = ArticleSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    filterset_class= ArticleFilter

    def get_queryset(self):
        queryset = Article.objects.all()
        if is_expanded(self.request, 'gros'):
            queryset = queryset.prefetch_related('gros')
        if is_expanded(self.request, 'client'):
            queryset = queryset.prefetch_related('client')
        if is_expanded(self.request, 'transitaire'):
            queryset = queryset.prefetch_related('transitaire')
        return queryset
    
    def list(self, request, *args, **kwargs):
        # Check if the 'all' parameter is present in the request query parameters
        if request.query_params.get('all', False):
            # If 'all' is present, return all records without pagination
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        # If 'all' is not present, proceed with pagination as usual
        return super().list(request, *args, **kwargs)


    @action(detail=False, methods=['post'])
    def bulk_delete(self, request, *args, **kwargs):
        ids = request.data.get('ids', [])
        if not ids:
           return Response({'detail': 'No IDs provided for deletion.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
           queryset = self.filter_queryset(self.get_queryset())
           deleted, _ = queryset.filter(pk__in=ids).delete()
           if deleted > 0:
               return Response({'detail': f'Successfully deleted objects with ids: {ids} .'}, status=status.HTTP_204_NO_CONTENT)
           else:
               return Response({'detail': 'No objects found for deletion.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
           return Response({'detail': f'Error during deletion: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    serializer_class = PositionSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    filterset_class= PositionFilter

    def get_queryset(self):
        queryset = Position.objects.all()
        if is_expanded(self.request, 'parc'):
            queryset = queryset.prefetch_related('parc')
        if is_expanded(self.request, 'zone'):
            queryset = queryset.prefetch_related('zone')
        if is_expanded(self.request, 'tc'):
            queryset = queryset.prefetch_related('tc')
        return queryset

    def list(self, request, *args, **kwargs):
        # Check if the 'all' parameter is present in the request query parameters
        if request.query_params.get('all', False):
            # If 'all' is present, return all records without pagination
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        # If 'all' is not present, proceed with pagination as usual
        return super().list(request, *args, **kwargs)


    @action(detail=False, methods=['post'])
    def bulk_delete(self, request, *args, **kwargs):
        ids = request.data.get('ids', [])
        if not ids:
           return Response({'detail': 'No IDs provided for deletion.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
           queryset = self.filter_queryset(self.get_queryset())
           deleted, _ = queryset.filter(pk__in=ids).delete()
           if deleted > 0:
               return Response({'detail': f'Successfully deleted objects with ids: {ids} .'}, status=status.HTTP_204_NO_CONTENT)
           else:
               return Response({'detail': 'No objects found for deletion.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
           return Response({'detail': f'Error during deletion: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class BulletinsEscortViewSet(viewsets.ModelViewSet):
    queryset = BulletinsEscort.objects.all()
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    serializer_class = BulletinsEscortSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    filterset_class= BulletinsEscortFilter

    def get_queryset(self):
        queryset = BulletinsEscort.objects.all()
        if is_expanded(self.request, 'gros'):
            queryset = queryset.prefetch_related('gros')
        if is_expanded(self.request, 'charge_chargement'):
            queryset = queryset.prefetch_related('charge_chargement')
        if is_expanded(self.request, 'charge_reception'):
            queryset = queryset.prefetch_related('charge_reception')
        return queryset
    
    def list(self, request, *args, **kwargs):
        # Check if the 'all' parameter is present in the request query parameters
        if request.query_params.get('all', False):
            # If 'all' is present, return all records without pagination
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        # If 'all' is not present, proceed with pagination as usual
        return super().list(request, *args, **kwargs)


    @action(detail=False, methods=['post'])
    def bulk_delete(self, request, *args, **kwargs):
        ids = request.data.get('ids', [])
        if not ids:
           return Response({'detail': 'No IDs provided for deletion.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
           queryset = self.filter_queryset(self.get_queryset())
           deleted, _ = queryset.filter(pk__in=ids).delete()
           if deleted > 0:
               return Response({'detail': f'Successfully deleted objects with ids: {ids} .'}, status=status.HTTP_204_NO_CONTENT)
           else:
               return Response({'detail': 'No objects found for deletion.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
           return Response({'detail': f'Error during deletion: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TcViewSet(viewsets.ModelViewSet):
    queryset = Tc.objects.all()
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    serializer_class = TcSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    filterset_class= TcFilter

    def get_queryset(self):
        queryset = Tc.objects.all()
        if is_expanded(self.request, 'article'):
            queryset = queryset.prefetch_related('article')
        if is_expanded(self.request, 'type_tc'):
            queryset = queryset.prefetch_related('type_tc')
        if is_expanded(self.request, 'bulletins'):
            queryset = queryset.prefetch_related('bulletins')
        if is_expanded(self.request, 'receved_by'):
            queryset = queryset.prefetch_related('receved_by')
        if is_expanded(self.request, 'current_scelle'):
            queryset = queryset.prefetch_related('current_scelle')
        return queryset
    
    def list(self, request, *args, **kwargs):
        # Check if the 'all' parameter is present in the request query parameters
        if request.query_params.get('all', False):
            # If 'all' is present, return all records without pagination
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        # If 'all' is not present, proceed with pagination as usual
        return super().list(request, *args, **kwargs)


    @action(detail=False, methods=['post'])
    def bulk_delete(self, request, *args, **kwargs):
        ids = request.data.get('ids', [])
        if not ids:
           return Response({'detail': 'No IDs provided for deletion.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
           queryset = self.filter_queryset(self.get_queryset())
           deleted, _ = queryset.filter(pk__in=ids).delete()
           if deleted > 0:
               return Response({'detail': f'Successfully deleted objects with ids: {ids} .'}, status=status.HTTP_204_NO_CONTENT)
           else:
               return Response({'detail': 'No objects found for deletion.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
           return Response({'detail': f'Error during deletion: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SousArticleViewSet(viewsets.ModelViewSet):
    queryset = SousArticle.objects.all()
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    serializer_class = SousArticleSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    filterset_class= SousArticleFilter

    def get_queryset(self):
        queryset = SousArticle.objects.all()
        if is_expanded(self.request, 'tc'):
            queryset = queryset.prefetch_related('tc')
        if is_expanded(self.request, 'client'):
            queryset = queryset.prefetch_related('client')
        if is_expanded(self.request, 'transitaire'):
            queryset = queryset.prefetch_related('transitaire')
        if is_expanded(self.request, 'box'):
            queryset = queryset.prefetch_related('box')
        return queryset
    
    def list(self, request, *args, **kwargs):
        # Check if the 'all' parameter is present in the request query parameters
        if request.query_params.get('all', False):
            # If 'all' is present, return all records without pagination
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        # If 'all' is not present, proceed with pagination as usual
        return super().list(request, *args, **kwargs)


    @action(detail=False, methods=['post'])
    def bulk_delete(self, request, *args, **kwargs):
        ids = request.data.get('ids', [])
        if not ids:
           return Response({'detail': 'No IDs provided for deletion.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
           queryset = self.filter_queryset(self.get_queryset())
           deleted, _ = queryset.filter(pk__in=ids).delete()
           if deleted > 0:
               return Response({'detail': f'Successfully deleted objects with ids: {ids} .'}, status=status.HTTP_204_NO_CONTENT)
           else:
               return Response({'detail': 'No objects found for deletion.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
           return Response({'detail': f'Error during deletion: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VisiteViewSet(viewsets.ModelViewSet):
    queryset = Visite.objects.all()
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    serializer_class = VisiteSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    filterset_class= VisiteFilter

    def get_queryset(self):
        queryset = Visite.objects.all()
        if is_expanded(self.request, 'gros'):
            queryset = queryset.prefetch_related('gros')
        if is_expanded(self.request, 'article'):
            queryset = queryset.prefetch_related('article')
        if is_expanded(self.request, 'transitaire'):
            queryset = queryset.prefetch_related('transitaire')
        return queryset
    
    def list(self, request, *args, **kwargs):
        # Check if the 'all' parameter is present in the request query parameters
        if request.query_params.get('all', False):
            # If 'all' is present, return all records without pagination
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        # If 'all' is not present, proceed with pagination as usual
        return super().list(request, *args, **kwargs)


    @action(detail=False, methods=['post'])
    def bulk_delete(self, request, *args, **kwargs):
        ids = request.data.get('ids', [])
        if not ids:
           return Response({'detail': 'No IDs provided for deletion.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
           queryset = self.filter_queryset(self.get_queryset())
           deleted, _ = queryset.filter(pk__in=ids).delete()
           if deleted > 0:
               return Response({'detail': f'Successfully deleted objects with ids: {ids} .'}, status=status.HTTP_204_NO_CONTENT)
           else:
               return Response({'detail': 'No objects found for deletion.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
           return Response({'detail': f'Error during deletion: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VisiteItemViewSet(viewsets.ModelViewSet):
    queryset = VisiteItem.objects.all()
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    serializer_class = VisiteItemSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    filterset_class= VisiteItemFilter

    def get_queryset(self):
        queryset = VisiteItem.objects.all()
        if is_expanded(self.request, 'visite'):
            queryset = queryset.prefetch_related('visite')
        if is_expanded(self.request, 'tc'):
            queryset = queryset.prefetch_related('tc')
        return queryset
    
    def list(self, request, *args, **kwargs):
        # Check if the 'all' parameter is present in the request query parameters
        if request.query_params.get('all', False):
            # If 'all' is present, return all records without pagination
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        # If 'all' is not present, proceed with pagination as usual
        return super().list(request, *args, **kwargs)


    @action(detail=False, methods=['post'])
    def bulk_delete(self, request, *args, **kwargs):
        ids = request.data.get('ids', [])
        if not ids:
           return Response({'detail': 'No IDs provided for deletion.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
           queryset = self.filter_queryset(self.get_queryset())
           deleted, _ = queryset.filter(pk__in=ids).delete()
           if deleted > 0:
               return Response({'detail': f'Successfully deleted objects with ids: {ids} .'}, status=status.HTTP_204_NO_CONTENT)
           else:
               return Response({'detail': 'No objects found for deletion.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
           return Response({'detail': f'Error during deletion: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ScelleViewSet(viewsets.ModelViewSet):
    queryset = Scelle.objects.all()
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    serializer_class = ScelleSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    filterset_class= ScelleFilter

    def get_queryset(self):
        queryset = Scelle.objects.all()
        if is_expanded(self.request, 'tc'):
            queryset = queryset.prefetch_related('tc')
        return queryset
    
    def list(self, request, *args, **kwargs):
        # Check if the 'all' parameter is present in the request query parameters
        if request.query_params.get('all', False):
            # If 'all' is present, return all records without pagination
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        # If 'all' is not present, proceed with pagination as usual
        return super().list(request, *args, **kwargs)


    @action(detail=False, methods=['post'])
    def bulk_delete(self, request, *args, **kwargs):
        ids = request.data.get('ids', [])
        if not ids:
           return Response({'detail': 'No IDs provided for deletion.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
           queryset = self.filter_queryset(self.get_queryset())
           deleted, _ = queryset.filter(pk__in=ids).delete()
           if deleted > 0:
               return Response({'detail': f'Successfully deleted objects with ids: {ids} .'}, status=status.HTTP_204_NO_CONTENT)
           else:
               return Response({'detail': 'No objects found for deletion.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
           return Response({'detail': f'Error during deletion: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

