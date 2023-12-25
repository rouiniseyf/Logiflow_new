from app.views.article_view import article_details
from ..models import *
from ..forms import *
from django.core.paginator import Paginator , PageNotAnInteger , EmptyPage
from django.shortcuts import render, redirect
from django.db.models import Q, Value 
from django.contrib import messages 
from django.http import JsonResponse,HttpResponseRedirect
from django.urls import reverse
from reference.models import * 
from bareme.models import *
from reference.forms import * 
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import F


@login_required(login_url='login')
@user_passes_test(lambda u: u.groups.filter(name='TRANSIT').exists(),login_url='access_denied')
def gros_details(request, pk):
    res = Gros.objects.filter(id=pk)
    selected_gros = res.values("id","gros","accostage","regime__designation","armateur__raison_sociale","consignataire__raison_sociale","navire__nom").first()

    search = request.GET.get('search')
    form_article = ArticleForm(initial={'gros': res.first()})   

    if request.method == 'POST':
            form = ArticleForm(request.POST)
            #if the form is vaid then save the Tc object and create the success message 
            if form.is_valid():
                form.save()
                messages.success(request,"Success",extra_tags="success")
                return HttpResponseRedirect(reverse("gros_details",args=(pk,)))

            else :
                messages.error(request,"Erreur", extra_tags="danger")

    if search != None and search != "": 
        form = SearchForm(request.GET)
        if form.is_valid(): 
            form = SearchForm(initial={'search': search})
            articles = Article.objects.filter(gros_id=pk).filter(
                Q(numero__icontains=search) 
                | Q(client__raison_sociale__icontains=search)
                ).order_by('numero').values("id","numero","bl","client__raison_sociale","designation")
            context = {
                'gros':selected_gros,
                'articles': articles,
                'form': form, 
                'form_article': form_article,
            }
            return render(request,'app/pages/gros_details.html',context)
    
    else: 
        form = SearchForm()
        articles = Article.objects.filter(gros_id=selected_gros["id"]).order_by('numero').values("id","numero","bl","client__raison_sociale","designation")
        page = request.GET.get('page',1)
        if page == "all": 
            context = {
                'gros':selected_gros, 
                'articles': articles,
                'form': form, 
                'form_article': form_article,
            }
            return render(request,"app/pages/gros_details.html",context)
        else:   
            paginator = Paginator(articles,7)
            try: 
                recoreds = paginator.page(page)
            except PageNotAnInteger: 
                recoreds = paginator.page(1)
            except EmptyPage : 
                recoreds = paginator.page(paginator.num_pages)
            context = {
                'gros':selected_gros,
                'articles': recoreds,
                'form': form, 
                'form_article': form_article,
            }
            return render(request,"app/pages/gros_details.html",context)

@login_required(login_url='login')
@user_passes_test(lambda u: u.groups.filter(name='TRANSIT').exists(),login_url='access_denied')
def gros_view(request):
    if request.method == 'POST':     
        form = GrosForm(request.POST)
        if form.is_valid() : 
            posted_gros = GrosForm(request.POST)
            instance = posted_gros.save()
            messages.success(request,"Success",extra_tags="success")
            return HttpResponseRedirect(reverse("gros_details",args=(instance.id,)))
        else :
            messages.error(request,"Une erreur s'est produite lors de l'ajout de gros", extra_tags="danger")
            
    form_gros = GrosForm(initial={'port_reception' :Port.objects.filter(Q(pays__nom_fr_fr__icontains='alger')|Q(pays__nom_fr_fr__icontains='Algérie')).filter(Q(raison_sociale__icontains='ALGE')).first()})
    port_form = PortForm()
    navire_form = NavireForm()
    armateur_form = ArmateurForm()
    consignataire_form = ConsignataireForm()

    search = request.GET.get('search')
    if search != None and search != "": 
        form = SearchForm(request.GET)
        if form.is_valid(): 
            form = SearchForm(initial={'search': search})
            queryset = Gros.objects.filter(
                Q(gros__icontains=search) 
                | Q(escale__icontains=search) 
                | Q(accostage__icontains=search) 
                | Q(port_emission__raison_sociale__icontains=search) 
                | Q(port_reception__raison_sociale__icontains=search) 
                | Q(navire__nom__icontains=search) 
                | Q(armateur__raison_sociale__icontains=search) 
                | Q(consignataire__raison_sociale__icontains=search)   
                ).values("id","gros","regime__designation","accostage","navire__nom","armateur__raison_sociale","consignataire__raison_sociale")
            
            context = {
                'data': queryset,
                'form_gros': form_gros,
                'port_form': port_form,
                'navire_form':navire_form,
                'armateur_form':armateur_form,
                'consignataire_form':consignataire_form,
            }
            return render(request,'app/pages/gros.html',context)
    else:        
        form = SearchForm()
        recoreds = Gros.objects.all().order_by("-id").values("id","gros","regime__designation","accostage","navire__nom","armateur__raison_sociale","consignataire__raison_sociale")

        page = request.GET.get('page',1)
        if page == "all": 
            context = {
                'data':recoreds,
                'search_form': form,
                'form_gros': form_gros,
                'port_form': port_form,
                'navire_form':navire_form,
                'armateur_form':armateur_form,
                'consignataire_form':consignataire_form,
            }
            return render(request,"app/pages/gros.html", context)
        else:   
            paginator = Paginator(recoreds,10)
            try: 
                recoreds = paginator.page(page)
            except PageNotAnInteger: 
                recoreds = paginator.page(1)
            except EmptyPage : 
                recoreds = paginator.page(paginator.num_pages)
    context = {
        'data':recoreds,
        'search_form': form,
        'form_gros': form_gros,
        'port_form': port_form,
        'navire_form':navire_form,
        'armateur_form':armateur_form,
        'consignataire_form':consignataire_form,
    }
    return render(request, "app/pages/gros.html", context)

@login_required(login_url='login')
@user_passes_test(lambda u: u.groups.filter(name='TRANSIT').exists(),login_url='access_denied')
def manifest(request, pk): 
    manifest = Tc.objects.filter(article__gros__id = pk)
    gros = Gros.objects.get(id=pk)
    types = Type.objects.all()
    context = {
        'gros' : gros,
        'manifest' : manifest , 
        'types' : types, 
    }
    return render(request, 'app/pages/manifest.html', context )

 
@login_required(login_url='login')
def get_manifest(request):
    if   request.method == "GET":
        selected_gros_id = request.GET.get("id")
        records = Tc.objects.filter(article__gros__id=selected_gros_id).order_by('-article').values(
            "id",
            "article_id",
            "article",
            "article__numero",
            "tc",
            "tar",
            "type_tc__designation",
            "poids",
            "article__client__id",
            "article__client__raison_sociale",
            "article__transitaire__id",
            "article__transitaire__raison_sociale",
            )
        serialized_records = []
        for record in records : 
            serialized_records.append(record)
        return JsonResponse({"data": serialized_records }, status=200)

    else:
        return JsonResponse({"error": "Somthing wrong",}, status=400)

@login_required(login_url='login')
def delete_gros(request):
    if   request.method == "POST":
        gros_id = request.POST.get('gros_id')
        articles = Article.objects.filter(gros__id=gros_id)
        if len(articles) == 0:
            gros = Gros.objects.get(id=int(gros_id))
            gros.delete()
            return JsonResponse({"message": "success",})
        else: 
            return JsonResponse({"message": "error",})