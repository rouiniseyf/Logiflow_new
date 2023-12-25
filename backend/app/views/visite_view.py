from typing import ContextManager
from ..models import *
from ..forms import *
from django.core.paginator import Paginator , PageNotAnInteger , EmptyPage
from django.db.models import Q, Value, query 
from django.contrib import messages 
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
import json
from django.views.generic import View
#importing get_template from loader
from django.template.loader import get_template
#import render_to_pdf from util.py 
from ..utils import render_to_pdf 
from reference.models import * 
from bareme.models import *
from reference.forms import * 
from django.contrib.auth.decorators import login_required, user_passes_test
import xlwt
from datetime import datetime,date

@login_required(login_url='login')
@user_passes_test(lambda u: u.groups.filter(name='FRANTOFFICE').exists(),login_url='access_denied')
def visite(request): 
    records = Visite.objects.all().order_by("-id")
    enattente = Visite.objects.filter(date_visite__gte=date.today())
    gros = Gros.objects.all()
    form_transitaire = TransitaireForm()
    transitaires = Transitaire.objects.all()
    search = request.GET.get('search')
    form_visite = VisiteForm()
    if search != None and search != "": 
        form = SearchForm(request.GET)
        if form.is_valid(): 
            form = SearchForm(initial={'search': search})
            records = Visite.objects.filter(
                Q(numero__icontains=search) 
                | Q(date_visite__icontains=search)
                | Q(gros__gros__icontains=search)
                | Q(type_visite__icontains=search)
                | Q(transitaire__raison_sociale__icontains=search)
                ).order_by('numero')
            context = {
                'enattente': enattente,
                'records' : records,
                'form': form, 
                'form_transitaire' : form_transitaire,
                'gros': gros,
                'transitaires' : transitaires , 
                'form_visite' : form_visite ,
            }
            return render(request,'app/pages/visite.html',context)
    
    else: 
        form = SearchForm()
        page = request.GET.get('page',1)
        if page == "all": 
            context = {
                'enattente': enattente,
                'records' : records,
                'form': form, 
                'form_transitaire' : form_transitaire,
                'gros': gros,
                'transitaires' : transitaires ,  
                'form_visite' : form_visite ,

            }
            return render(request, 'app/pages/visite.html', context)
        else:   
            paginator = Paginator(records,11)
            try: 
                records = paginator.page(page)
            except PageNotAnInteger: 
                records = paginator.page(1)
            except EmptyPage : 
                records = paginator.page(paginator.num_pages)
                 
            context = { 
                'enattente': enattente,
                'records' : records,
                'form': form, 
                'form_transitaire' : form_transitaire,
                'gros': gros,
                'transitaires' : transitaires ,  
                'form_visite' : form_visite ,
            }   
            return render(request, 'app/pages/visite.html', context)

@login_required(login_url='login')
@user_passes_test(lambda u: u.groups.filter(name='FRANTOFFICE').exists(),login_url='access_denied')
def visite_details(request, pk): 

    visite = Visite.objects.get(id=pk)

    return render(request, 'app/pages/visite_details.html', {
        "visite" : visite,
        "visite_items" : visite.get_items(),
    })

@login_required(login_url='login')
def save_visite(request): 
    if   request.method == "POST":
        saved_data = request.POST.get('saved_data')
        visite_id = int(request.POST.get('visite'))
        selected_visite = Visite.objects.get(pk=visite_id)
        data = json.loads(saved_data)
       
        for item in data : 
            id = item["id"]
            tc = Tc.objects.get(pk=id)
            new_scelle = Scelle.objects.create(numero = item["scelle"],tc = tc , type_scelle="scelle_visite") 
            Tc.objects.filter(pk=id).update(current_scelle =  new_scelle)
            VisiteItem.objects.create(
                visite = selected_visite,
                tc =  tc,
                scelle = item["scelle"],
                observation = item["observation"], 
            )


        return JsonResponse({"message": "success",})


@login_required(login_url='login')
@user_passes_test(lambda u: u.groups.filter(name='FRANTOFFICE').exists(),login_url='access_denied')
def print_visite(request,pk):
    visite = Visite.objects.get(id=pk) 
    visite_items = VisiteItem.objects.filter(visite__id=visite.id)
    positions = [ item.tc.get_current_position() for item in visite.get_items() if item.tc.get_current_position()  ]


    pdf = render_to_pdf('app/reporting/visite.html', {
        "visite" : visite,
        "visite_items" : visite.get_items(),
        "positions" : positions,
    }  )
       
    #rendering the template
    return HttpResponse(pdf, content_type='application/pdf')

@login_required(login_url='login')
@user_passes_test(lambda u: u.groups.filter(name='FRANTOFFICE').exists(),login_url='access_denied')
def calendrier(request): 
    todays_visits  = Visite.objects.filter(date_visite = date.today())
    context = {
        'todays_visits' : todays_visits,
    }
    return render(request,'app/pages/calendrier.html', context)

@login_required(login_url='login')
def get_visits_by_month(request): 

    if request.method == "GET":

        items = Visite.objects.filter(
            date_visite__month = int(request.GET.get('selected_month')), 
            date_visite__year = int(request.GET.get('selected_year'))
            )
 
        visites = items.values(
            'id', 
            'visite',
            'numero', 
            'date_visite',
            'gros', 
            'article',
            'article__client__raison_sociale',
            'article__designation',
            'type_visite', 
            'transitaire', 
            'badge'
        ) 


        return JsonResponse({"data": serialize(visites)}, status=200)


@login_required(login_url='login')
def get_transitaires(request): 

    if   request.method == "GET":
        return JsonResponse({"data": serialize(Transitaire.objects.all().values('id', 'raison_sociale',) )}, status=200)

        
@login_required(login_url='login')
def get_contaienrs_by_visite(request): 
    if   request.method == "GET":
        selected_visit = int(request.GET.get('selected_visit'))

        containers = VisiteItem.objects.filter(visite__id = selected_visit).values('id','tc__id','tc__tc','tc__article__numero','tc__type_tc__designation','scelle')

        return JsonResponse({"data": serialize(containers)}, status=200)


@login_required(login_url='login')
def update_visite(request): 
    if   request.method == "POST":
        selected_date = request.POST.get('selected_date')
        selected_transitaire = int(request.POST.get('selected_transitaire'))
        visit = int(request.POST.get('visite'))

        Visite.objects.filter(pk=visit).update(transitaire=Transitaire.objects.get(pk=selected_transitaire), date_visite=selected_date)
 
    return JsonResponse({"message": "success", }, status=200)


@login_required(login_url='login')
def update_scelle(request): 
    if   request.method == "POST":
        tc = int(request.POST.get('tc'))
        scelle = int(request.POST.get('scelle'))
        VisiteItem.objects.filter(tc__id=tc).update(scelle = scelle)

    return JsonResponse({"message": "success", }, status=200)

@login_required(login_url='login')
def export_excel_todays_visites(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('data')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Visite','Tc','Scelle','Transitaire',"Badge","Observation" ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    visites  = Visite.objects.filter(date_visite = date.today()).values_list("id")
    #rows = []
    #for item in visites : 
    rows = VisiteItem.objects.filter(visite__id__in = visites).values_list("visite__visite","tc","scelle","visite__transitaire__raison_sociale","visite__badge","observation")

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


@login_required(login_url='login')
@user_passes_test(lambda u: u.groups.filter(name='FRANTOFFICE').exists(),login_url='access_denied')
def print_todays_visites(request):

    visites  = Visite.objects.filter(date_visite = date.today()).values_list("id")
    rows = VisiteItem.objects.filter(visite__id__in = visites).order_by('tc__type_tc')

    context = {
        "rows" : rows,
        "date" : date.today(),
        "cuurent_user" : request.user
    }  

    #getting the template
    pdf = render_to_pdf('app/reporting/todays_visite.html', context)
       
        #rendering the template
    return HttpResponse(pdf, content_type='application/pdf')

@login_required(login_url='login')
@user_passes_test(lambda u: u.groups.filter(name='FRANTOFFICE').exists(),login_url='access_denied')
def print_selected_day_visites(request, date):

  
    visites  = Visite.objects.filter(date_visite = datetime.strptime(date, '%Y-%m-%d')).values_list("id")
    rows = VisiteItem.objects.filter(visite__id__in = visites)

    context = {
        "rows" : rows,
        "date" : date,
        "cuurent_user" : request.user
    }  

    #getting the template
    pdf = render_to_pdf('app/reporting/todays_visite.html', context)
       
        #rendering the template
    return HttpResponse(pdf, content_type='application/pdf')


    