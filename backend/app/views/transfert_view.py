from ..models import *
from ..forms import *
from django.core.paginator import Paginator , PageNotAnInteger , EmptyPage
from django.shortcuts import render, redirect
from django.db.models import Q, Value 
from django.contrib import messages 
from django.http import JsonResponse,HttpResponseRedirect
from django.urls import reverse
import json
from django.contrib.auth.models import User
from reference.models import * 
from bareme.models import *
from reference.forms import * 
from django.contrib.auth.decorators import login_required, user_passes_test
from billing.models import BonSortieItem,BonSortie
from datetime import timezone

def has_lines(selected_bulletins): 
    if Tc.objects.all().filter(bulletins=selected_bulletins).count() > 0: 
        return True 
    else : 
        return False 

@login_required(login_url='login')
def chargement(request):
    records = BulletinsEscort.objects.all().order_by('-id')
    for item in records: 
        if item.has_lines == False: 
            item.delete()
            
    form_bulletins = BulletinsEscortForm()
    search = request.GET.get('search')
    form_agent = AgentForm() 
    if request.method == 'POST':
            form = BulletinsEscortForm(request.POST)
            #if the form is vaid then save the Bulletins object and create the success message 
            if form.is_valid():
                instance = form.instance
                instance.charge_chargement = request.user
                result = form.save()
                articles = Article.objects.filter(gros=result.gros).order_by('numero')
                form = BulletinsEscortForm(instance= result)
                context = {
                    'bulletins': result,
                    'articles' : articles, 
                    'form' : form,
                }
                return render(request, 'app/pages/bulletins_details.html', context) 
            else :
                messages.error(request,"Le gros sélectionné n'a pas d'articles avec des contenants non reçus.", extra_tags="danger")

    if search != None and search != "": 
        form = SearchForm(request.GET)
        if form.is_valid(): 
            form = SearchForm(initial={'search': search})
            records = BulletinsEscort.objects.filter(
                Q(bulletins__icontains=search) 
                | Q(date_creation__icontains=search)
                | Q(gros__gros__icontains=search)
                | Q(charge_chargement__first_name__icontains=search)
                | Q(charge_chargement__last_name__icontains=search)
                ).order_by('numero')
            context = {
                'records' : records,
                'form': form, 
                'form_bulletins': form_bulletins,
                'form_agent': form_agent,
            }
            return render(request,'app/pages/chargement.html',context)
    
    else: 
        form = SearchForm()
        page = request.GET.get('page',1)
        if page == "all": 
            context = {
                'records' : records,
                'form': form, 
                'form_bulletins': form_bulletins,
                'form_agent': form_agent,
            }
            return render(request, 'app/pages/chargement.html', context)
        else:   
            paginator = Paginator(records,11)
            try: 
                records = paginator.page(page)
            except PageNotAnInteger: 
                records = paginator.page(1)
            except EmptyPage : 
                records = paginator.page(paginator.num_pages)


            context = { 

                'records' : records,
                'form': form, 
                'form_bulletins' : form_bulletins,
                'form_agent': form_agent, 
            } 
                
            return render(request, 'app/pages/chargement.html', context)


@login_required(login_url='login')
def update_bulletins(request, pk): 
    item = BulletinsEscort.objects.get(id=pk)   
    form = BulletinsEscort(instance=item)
    if request.method == 'POST' :
        form = BulletinsEscortForm(request.POST,instance=item)
        if form.is_valid(): 
            form.save()  
            messages.success(request,"Successfully updated. ",extra_tags="success")
            return redirect('/chargement')

@login_required(login_url='login')
@user_passes_test(lambda u: u.groups.filter(name='TRANSIT').exists(),login_url='access_denied')
def bulletins_details(request, pk):
    selected_bulletins = BulletinsEscort.objects.get(id=pk)
    articles = Article.objects.filter(gros=selected_bulletins.gros).order_by('numero')
    form = BulletinsEscortForm(instance= selected_bulletins)
    context = {
        'bulletins': selected_bulletins,
        'articles' : articles, 
        'form' : form,
        'is_mobile' : request.user_agent.is_mobile
    }


    if request.method == 'POST' :
        form = BulletinsEscortForm(request.POST,instance=selected_bulletins)
        if form.is_valid(): 
            form.save()  
            messages.success(request,"Successfully updated. ",extra_tags="success")
            return render(request, 'app/pages/bulletins_details.html', context) 


    return render(request, 'app/pages/bulletins_details.html', context) 

@login_required(login_url='login')
def delete_bulletins(request):
    if   request.method == "POST":
        bulletins_id = request.POST.get('bulletins_id')
        bulletins = BulletinsEscort.objects.get(id=int(bulletins_id))
        bulletins.delete()
        return JsonResponse({"message": "success",})

@login_required(login_url='login')
@user_passes_test(lambda u: u.groups.filter(name='BACKOFFICE').exists(),login_url='access_denied')
def reception_details(request, pk):
    selected_bulletins = BulletinsEscort.objects.get(id=pk)
    records = Tc.objects.filter(article__gros=selected_bulletins.gros).order_by('article__numero')

    parcs = [{"designation": parc.designation,"id":parc.id, "zones": [{"zone": zone.zone,"id":zone.id,"parc":parc} for zone in parc.zone_set.all().order_by("id")]} for parc in Parc.objects.all()]
    zones = Zone.objects.all()

    context = {
        'bulletins': selected_bulletins,
        'user' : request.user, 
        'records' : records,
        'parcs' : parcs,
        'zones' : zones,
        'is_mobile' : request.user_agent.is_mobile
    }
    return render(request, 'app/pages/reception_details.html', context) 

@login_required(login_url='login')
@user_passes_test(lambda u: u.groups.filter(name='BACKOFFICE').exists(),login_url='access_denied')
def reception(request): 
    all_bulletins = BulletinsEscort.objects.all().filter(loaded=True).order_by("-id")
    search = request.GET.get('search')
    waiting_bulletins = BulletinsEscort.objects.filter(receved=False,loaded=True).order_by("id")
    filterd_waiting_list = []
    records = []
    for bulletins in waiting_bulletins: 
        if (has_lines(bulletins)): 
            filterd_waiting_list.append(bulletins)

    for bulletins in all_bulletins: 
        if (has_lines(bulletins)): 
            records.append(bulletins)
    if search != None and search != "": 
        form = SearchForm(request.GET)
        if form.is_valid(): 
            form = SearchForm(initial={'search': search})
            records = BulletinsEscort.objects.filter(
                Q(bulletins__icontains=search) 
                | Q(date_creation__icontains=search)
                | Q(gros__gros__icontains=search)
                | Q(charge_chargement__first_name__icontains=search)
                | Q(charge_reception__last_name__icontains=search)
                ).order_by('numero')
            context = {
                'waiting_bulletins': filterd_waiting_list,
                'records' : records,
                'form': form, 
            }
            return render(request,'app/pages/reception.html',context)
    
    else: 
        form = SearchForm()
        page = request.GET.get('page',1)
        if page == "all": 
            context = {
                'waiting_bulletins': filterd_waiting_list,
                'records' : records,
                'form': form, 
            }
            return render(request, 'app/pages/reception.html', context)
        else:   
            paginator = Paginator(records,11)
            try: 
                records = paginator.page(page)
            except PageNotAnInteger: 
                records = paginator.page(1)
            except EmptyPage : 
                records = paginator.page(paginator.num_pages)
                 
            context = { 
                'waiting_bulletins': filterd_waiting_list,
                'records' : records,
                'form': form, 
            }   
            return render(request, 'app/pages/reception.html', context)


@login_required(login_url='login')
def save_chargement(request): 
    if   request.method == "POST":
        saved_data = request.POST.get('saved_data')
        bulletins = BulletinsEscort.objects.get(pk=int(request.POST.get('bulletins')))
        data = json.loads(saved_data)
        for item in data : 
            pk = item["id"]
            tc = Tc.objects.get(id=pk)
            matricule = item["matricule"]
            date = item["date"]
            observation = item["observation"]
            scelle = None

            if item["scelle"] != "":   
                current_scelle = tc.current_scelle  
                if current_scelle != None : 
                    if current_scelle.numero == item["scelle"] : 
                        scelle = current_scelle 
                    else: 
                        scelle = Scelle.objects.filter(tc = tc).update(numero = item["scelle"] )
                else : 
                    scelle = Scelle.objects.create(numero = item["scelle"],tc = tc , type_scelle="scelle_port") 
      
            Tc.objects.filter(id=pk).update(
                bulletins=bulletins,
                matricule_camion=matricule,
                current_scelle =  scelle,
                date_sortie_port=date,
                observation_chargement=observation
                )
        return JsonResponse({"message": "success",})

@login_required(login_url='login')
def validate_bulletins(request): 
    if   request.method == "POST":
        bulletins_id = int(request.POST.get('bulletins'))
        BulletinsEscort.objects.filter(id=bulletins_id).update(loaded=True)
        return JsonResponse({"message": "success",})

@login_required(login_url='login')
def save_reception(request): 
    if   request.method == "POST":
        saved_data = request.POST.get('saved_data')
        bulletins_id = int(request.POST.get('bulletins'))
        data = json.loads(saved_data)
        for item in data : 
            pk = item["id"]
            observation = item["observation"]
            Tc.objects.filter(id=pk).update(
                observation_reception=observation, 
                receved = True,
                receved_by = request.user
                )
        bulletins_tcs = Tc.objects.filter(bulletins = bulletins_id)
        BulletinsEscort.objects.filter(id=bulletins_id).update(charge_reception=request.user)

        all_receved = True 
        for item in bulletins_tcs : 
            if item.date_entree_port_sec is None : 
                all_receved = False
            
        if all_receved : 
            BulletinsEscort.objects.filter(id=bulletins_id).update(receved=True)


        return JsonResponse({"message": "success",})

@login_required(login_url='login')
def get_tcs_by_bulletins(request):
    if   request.method == "GET":
        selected_bulletins_id = request.GET.get("selected_bulletins_id")
        records = Tc.objects.filter(bulletins__id=selected_bulletins_id).values(
            "id",
            "article__numero",
            "tc",
            "tar",
            "type_tc__designation",
            "poids",
            "article__client__raison_sociale",
            "matricule_camion", 
            "current_scelle__numero",
            "date_sortie_port",
            "observation_chargement",
            )
        serialized_records = []
        for record in records : 
            serialized_records.append(record)
        return JsonResponse({"data": serialized_records }, status=200)

    else:
        return JsonResponse({"error": "Somthing happned",}, status=400)

    return JsonResponse({"error": ""}, status=400)

@login_required(login_url='login')
def get_reception(request):
    if   request.method == "GET":
        selected_bulletins_id = request.GET.get("selected_bulletins_id")
        records = Tc.objects.filter(bulletins__id=selected_bulletins_id).values(
            "id",
            "article__numero",
            "tc",
            "type_tc__designation",
            "matricule_camion", 
            "date_entree_port_sec",
            "observation_reception",
            "receved_by__first_name",
            "receved_by__last_name",
            "receved",
            )
        serialized_records = []
        for record in records : 
            serialized_records.append(record)
        
        return JsonResponse({"data": serialized_records }, status=200)

    else:
        return JsonResponse({"error": "Somthing happned",}, status=400)

    return JsonResponse({"error": ""}, status=400)

#Documentations 

# ---- Get the Groups of the current user 
#  l = request.user.groups.values_list('name',flat = True) # QuerySet Object
#  l_as_list = list(l)  

@login_required(login_url='login')
@user_passes_test(lambda u: u.groups.filter(name='SECURITE').exists(),login_url='access_denied')
def entree(request): 
    records = Tc.objects.charged().filter(date_entree_port_sec__isnull=True).order_by("date_sortie_port")
    
    search = request.GET.get('search')

    if search != None and search != "": 
        form = SearchForm(request.GET)
        if form.is_valid(): 
            form = SearchForm(initial={'search': search})
              
            records = Tc.objects.charged().filter(date_entree_port_sec__isnull=True).filter(Q(tc__icontains=search)).order_by('date_sortie_port')
            context = {
                'records' : records,
                'form': form, 
            }
            return render(request,'app/pages/entree.html',context)
    
    else: 
        form = SearchForm()
        page = request.GET.get('page',1)
        if page == "all": 
            context = {
                'records' : records,
                'form': form, 
            }
            return render(request, 'app/pages/entree.html', context)
        else:   
            paginator = Paginator(records,10)
            try: 
                records = paginator.page(page)
            except PageNotAnInteger: 
                records = paginator.page(1)
            except EmptyPage : 
                records = paginator.page(paginator.num_pages)
                 
            context = { 
                'records' : records,
                'form': form, 
            }   
            return render(request, 'app/pages/entree.html', context)

@login_required(login_url='login')
def entrer_port_sec(request):
    if   request.method == "POST":
        tc_id = int(request.POST.get("tc_id"))
        observation = request.POST.get("observation")

        Tc.objects.filter(pk= tc_id).update(date_entree_port_sec = datetime.datetime.now(), observation_entree_port_sec = observation)
        
        return JsonResponse({"message": "success",}, status=200)

    else:
        return JsonResponse({"error": "Somthing happned",}, status=400)

@login_required(login_url='login')
@user_passes_test(lambda u: u.groups.filter(name='SECURITE').exists(),login_url='access_denied')
def sortie(request): 
    records = BonSortieItem.objects.all().filter(tc__date_sortie_port_sec__isnull=True, tc__billed = True).order_by("bon_sortie")
    search = request.GET.get('search')

    if search != None and search != "": 
        form = SearchForm(request.GET)
        if form.is_valid(): 
            form = SearchForm(initial={'search': search})
              
            records = BonSortieItem.objects.all().filter(tc__date_sortie_port_sec__isnull=True, tc__billed = True).filter(Q(tc__tc__icontains=search)).order_by("bon_sortie")
            context = {
                'records' : records,
                'form': form, 
            }
            return render(request,'app/pages/sortie.html',context)
    
    else: 
        form = SearchForm()
        page = request.GET.get('page',1)
        if page == "all": 
            context = {
                'records' : records,
                'form': form, 
            }
            return render(request, 'app/pages/sortie.html', context)
        else:   
            paginator = Paginator(records,10)
            try: 
                records = paginator.page(page)
            except PageNotAnInteger: 
                records = paginator.page(1)
            except EmptyPage : 
                records = paginator.page(paginator.num_pages)
                 
            context = { 
                'records' : records,
                'form': form, 
            }   
            return render(request, 'app/pages/sortie.html', context)

@login_required(login_url='login')
def sortie_port_sec(request):
    if   request.method == "POST":
        tc_id = int(request.POST.get("tc_id"))
        observation = request.POST.get("observation")
        Tc.objects.filter(pk= tc_id).update(date_sortie_port_sec = datetime.datetime.now().replace(tzinfo=timezone.utc), observation_sortie_port_sec = observation)
        
        return JsonResponse({"message": "success",}, status=200)

    else:
        return JsonResponse({"error": "Somthing happned",}, status=400)



