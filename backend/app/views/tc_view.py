from ..models import *
from ..forms import *
from django.core.paginator import Paginator , PageNotAnInteger , EmptyPage
from django.shortcuts import render
from django.db.models import Q, Value 
from django.contrib import messages 
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required, user_passes_test
from reference.models import * 
from bareme.models import *
from reference.forms import * 


def container_charged(pk): 
    selected_container = Tc.objects.get(id=pk)
    if selected_container.bulletins is None: 
        return False 
    else :
        return True 


def containers_added_to_visite(article, visite): 
    added = VisiteItem.objects.filter(visite__id=visite)
    added_ids = []
    for item in added: 
        added_ids.append(item.tc.id)

    all_tcs = Tc.objects.filter(article__id=article).exclude(id__in=added_ids)
    return all_tcs
 
@login_required(login_url='login')
def update_dangereux(request):
    if   request.method == "GET":
        selected_tc = request.GET.get("tc")
        tc = Tc.objects.get(pk=selected_tc)

        if request.GET.get("checked_value") == 'true': 
            tc.dangereux = True
            tc.save()

        elif request.GET.get("checked_value") == 'false':
            tc.dangereux = False
            tc.save()

    return JsonResponse({"response": "okay"})

@login_required(login_url='login')
def update_sous_article_type(request):
    if request.method == "POST":
        _dangereux = request.POST.get("dangereux")
        sous_article_id = int(request.POST.get("sous_article_id"))

        if _dangereux == 'true': 
            _dangereux = True 
          
        if _dangereux == 'false': 
            _dangereux = False
        
        
        SousArticle.objects.filter(id = sous_article_id).update(dangereux = _dangereux)

    return JsonResponse({"response": "okay"})

login_required(login_url='login')
def tc_groupage_details(request, pk):

    selected_tc = Tc.objects.get(id=pk)
    sous_articles = SousArticle.objects.filter(tc=selected_tc)
    form_sous_article = SousArticleForm(initial={'tc': selected_tc})   

    if request.method == 'POST' and 'sous_article_submit' in request.POST:
        form = SousArticleForm(request.POST)
        #if the form is vaid then save the sousarticle object and create the success message 
        if form.is_valid():
            form.save()
            messages.success(request,"Success",extra_tags="success")
        else :
            messages.error(request,"Container already exist", extra_tags="danger")

    context = {
        'selected_tc': selected_tc, 
        'sous_articles' : sous_articles,
        'form_sous_article' : form_sous_article
    }
     
    return render(request,"app/pages/tc_details.html",context)

@login_required(login_url='login')
def update_type(request):
    if   request.method == "GET":
        selected_tc = request.GET.get("tc")
        tc = Tc.objects.get(pk=selected_tc)
        selected_type = Type.objects.get(pk=request.GET.get("selected_id"))
        tc.type_tc = selected_type
        tc.save()

    return JsonResponse({"response": "okay"})

@login_required(login_url='login')
def update_frigo(request):
    if   request.method == "GET":
        selected_tc = request.GET.get("tc")
        tc = Tc.objects.get(pk=selected_tc)

        if request.GET.get("checked_value") == 'true': 
            tc.frigo = True
            tc.save()

        elif request.GET.get("checked_value") == 'false':
            tc.frigo = False
            tc.save()

    return JsonResponse({"response": "okay"})

@login_required(login_url='login')
def set_type_class(request): 
    if   request.method == "POST":
        ids = request.POST.getlist('ids[]')
        selected_type = request.POST.get('selected_type')
        dangereux = request.POST.get('dangereux')
        frigo = request.POST.get('frigo')


        if selected_type != 'aucune sélection' :
            selected_type = Type.objects.get(pk=int(selected_type))
            Tc.objects.filter(id__in=ids).update(type_tc=selected_type,dangereux = dangereux, frigo = frigo)

    return JsonResponse({"message": "success", })

@login_required(login_url='login')
def get_not_loaded_tcs_by_article(request):
    if   request.method == "GET":
        selected_article_id = request.GET.get("selected_article_id")

        records = Tc.objects.filter(article__id=selected_article_id).values(
            "id",
            "article__numero",
            "tc",
            "tar",
            "type_tc__designation",
            "poids",
            "article__client__raison_sociale",

            )

        filterd_records = [] 
        # Return just the cotainers that haven't been loaded yet 
        for record in records :
            # Test if  the container is already loaded  
            if container_charged(record["id"]) == False: 
                filterd_records.append(record)

        return JsonResponse({"data": filterd_records }, status=200)

    else:
        return JsonResponse({"error": "Somthing happned",}, status=400)

@login_required(login_url='login')
def get_not_loaded_tcs_by_gros(request):
    if   request.method == "GET":
        gros = Gros.objects.get(id = int(request.GET.get("selected_gros")))

        records = gros.get_not_charged_containenrs().values(
            "id",
            "article__numero",
            "tc",
            "tar",
            "type_tc__designation",
            "poids",
            "article__client__raison_sociale",

            )

        filterd_records = [] 
        # Return just the cotainers that haven't been loaded yet 
        for record in records :
            # Test if  the container is already loaded  
            if container_charged(record["id"]) == False: 
                filterd_records.append(record)

        return JsonResponse({"data": filterd_records }, status=200)

    else:
        return JsonResponse({"error": "Somthing happned",}, status=400)

@login_required(login_url='login')
def get_not_added_to_visite_tcs(request):
    if   request.method == "GET":
        article = request.GET.get("article")
        visite = request.GET.get("visite")
        filtered_list = containers_added_to_visite(article,visite).values(
            "id",
            "article__numero",
            "tar",
            "tc",
            "type_tc__designation", 
            "dangereux", 
            "frigo"
        )
        filterd_records = [] 
        # Return just the cotainers that haven't been loaded yet 
        for record in filtered_list :
            filterd_records.append(record)

        return JsonResponse({"data": filterd_records }, status=200)

    else:
        return JsonResponse({"error": "Somthing happned",}, status=400)



@login_required(login_url='login')
def get_tcs_by_article(request):
    if   request.method == "GET":
        selected_article_id = request.GET.get("selected_article_id")
        article = Article.objects.get(id=selected_article_id)

        records = Tc.objects.filter(article__id=selected_article_id).values(
            "id",
            "article__numero",
            "article__designation",
            "tc",
            "tar",
            "type_tc__designation",
            "dangereux",
            "frigo",
            "poids",
            "article__client__raison_sociale",
            "date_sortie_port", 
            "date_entree_port_sec", 
            "article__gros__accostage",
            )
        vuaquai = True 
        for item in records: 
            if item["date_entree_port_sec"] == None : 
                vuaquai = False
        info = {
            'article' : article.numero, 
            'gros' : article.gros.gros,
            'client' : article.client.raison_sociale,
            'designation': article.designation,
            'vuaquai': vuaquai,
        }

        serialized_records = []
        for record in records : 
            serialized_records.append(record)

        return JsonResponse({"data": serialized_records, 'info': info}, status=200)

    else:
        return JsonResponse({"error": "Somthing happned",}, status=400)


@login_required(login_url='login')
def get_tcs_by_article_frais(request):
    if request.method == "GET":
        selected_article_id = request.GET.get("selected_article_id")
        article = Article.objects.get(id=selected_article_id)

        frais_portuaires = article.get_prestations_occasionnelle().filter(rubrique="FRAIS PORTUAIRES")
        immobilisation = article.get_prestations_occasionnelle().filter(rubrique="IMMOBILISATION")
        
        info = {
            'article' : article.numero, 
            'gros' : article.gros.gros,
            'regime' : article.gros.regime.designation,
            'client' : article.client.raison_sociale,
            'designation': article.designation,
            'frais_portuaires': get_sum_prix(frais_portuaires),
            'immobilisation': get_sum_prix(immobilisation)
        }

        return JsonResponse({'data': info}, status=200)

    else:
        return JsonResponse({"error": "Somthing happned",}, status=400)



@login_required(login_url='login')
def get_tcs_by_article_not_billed(request):
    if   request.method == "GET":
        selected_article_id = request.GET.get("selected_article_id")
        article = Article.objects.get(id=selected_article_id)

        records = Tc.objects.filter(article__id=selected_article_id).filter(billed=None).values(
            "id",
            "article__numero",
            "article__designation",
            "tc",
            "tar",
            "type_tc__designation",
            "dangereux",
            "frigo",
            "poids",
            "article__client__raison_sociale",
            "date_sortie_port", 
            "date_entree_port_sec", 
            "article__gros__accostage",
            )
        vuaquai = True 
        for item in records: 
            if item["date_entree_port_sec"] == None : 
                vuaquai = False
        info = {
            'article' : article.numero, 
            'gros' : article.gros.gros,
            'client' : article.client.raison_sociale,
            'vuaquai': vuaquai,
        }

        serialized_records = []
        for record in records : 
            serialized_records.append(record)

        return JsonResponse({"data": serialized_records, 'info': info}, status=200)

    else:
        return JsonResponse({"error": "Somthing happned",}, status=400)

@login_required(login_url='login')
def get_zones(request):
    if   request.method == "GET":
        selected_park = request.GET.get("selected_park")
  
        records = Zone.objects.filter(parc__id=selected_park).values(
            "id",
            "zone",
            )

        serialized_records = []
        for record in records : 
            serialized_records.append(record)

        return JsonResponse({"data": serialized_records}, status=200)

    else:
        return JsonResponse({"error": "Somthing happned",}, status=400)


@login_required(login_url='login')
@user_passes_test(lambda u: u.groups.filter(name='POINTEUR').exists(),login_url='access_denied')
def update_position(request): 
    search = request.GET.get('search')
    form = SearchForm(request.GET)
    queryset = []
    if search != None and search != "": 
        queryset = Tc.objects.all().filter(
            Q(tc__icontains=search) 
            ) 
    positions = [tc.get_current_position() for tc in queryset]

    context = {
       "data" : queryset,
       "form" : form,
       "positions" : positions,
    }

    return render(request, "app/pages/update_position.html", context)


@login_required(login_url='login')
@user_passes_test(lambda u: u.groups.filter(name='POINTEUR').exists(),login_url='access_denied')
def update_position_details(request,pk): 
    selected_tc = Tc.objects.get(id=pk)
    positions = Position.objects.filter(tc=selected_tc).order_by("-id")
    current_position = positions.first()
    form = PositionForm(instance=current_position)

    if len(positions) == 0:
        form = PositionForm(initial={'tc':selected_tc})
        

    if request.method == "POST" : 
        instance = PositionForm(request.POST)
        if instance.is_valid() : 
            current_position = instance.save() 
            messages.success(request,"Success",extra_tags="success")

        else: 
            messages.error(request,instance.errors, extra_tags="danger")

    positions = Position.objects.filter(tc=selected_tc).order_by("-id")

    context = {
        'selected_tc' : selected_tc,
        'positions' : positions,
        'current_position' : current_position,
        'form' : form,
    }
    return render(request,'app/pages/update_position_details.html',context)


