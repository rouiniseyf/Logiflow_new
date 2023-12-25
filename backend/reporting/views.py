import csv
import xlwt
from django.http import HttpResponse,FileResponse
from app.models import Tc
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.templatetags.static import static
from django.core.files.storage import default_storage
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from reference.models import *
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
import json

def export_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="somefilename.csv"'},
    )

    results = Tc.objects.all()
    writer = csv.writer(response)
    writer.writerow(['TC', 'Article', 'Gros', 'Client'])
    for item in results: 
        writer.writerow([item.tc, item.article, item.article.gros, item.article.client.raison_sociale,])

    return response


def alpha_export_excel(request):
    if   request.method == "POST":
        data =json.load(request)['data']

         
        
        #data = json.loads(loaded_data)

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="report.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('data')

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = data['headers']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        for row in data['data']:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

   
        wb.save(response)


        return response


def export_excel(request):

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('data')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Gros', 'Article', 'Gros', 'Client', ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Tc.objects.all().values_list("tc","article__numero", "article__gros","article__client__raison_sociale")
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

@login_required(login_url='login')
@user_passes_test(lambda u: u.groups.filter(name='REPORTING').exists(),login_url='access_denied')
def etat_facturation(request) : 
    context = {

        }

    return render(request, 'reporting/etat_de_facturation.html', context)


@login_required(login_url='login')
def get_tcs(request):
    if   request.method == "GET":
        selected_type = request.GET.get("selected_type")
        selected_class = request.GET.get("selected_class")
        starting_date = request.GET.get("starting_date")
        ending_date = request.GET.get("ending_date")

        records = Tc.objects.filter(date_entree__range=[starting_date, ending_date])
        
        if selected_type != "0":
            records.filter()

        
        # .values(
        #     "tc",
        #     "article__numero",
        #     "article__gros_numero",
        #     "type_tc__designation",
        #     "dangereux",
        #     "frigo",
        #     "poids",
        #     "article__client__raison_sociale",
        #     "article__Trnasitaire__raison_sociale",
        #     "date_sortie", 
        #     "date_entree", 
        #     "date_sortie_final", 
        #     )
     

        
        # info = {
        #     'article' : article.numero, 
        #     'gros' : article.gros.gros,
        #     'client' : article.client.raison_sociale,
        #     'vuaquai': vuaquai,
        # }

        info = {

        }
        serialized_records = []
        for record in records : 
            serialized_records.append(record)

        return JsonResponse({"data": serialized_records, 'info': info}, status=200)

    else:
        return JsonResponse({"error": "Somthing happned",}, status=400)




@login_required(login_url='login')
@user_passes_test(lambda u: u.groups.filter(name='REPORTING').exists(),login_url='access_denied')
def etat_tcs(request) : 
    
    types = Type.objects.all().order_by("id")
    context = {
        'types': types,
    }
    return render(request, 'reporting/etat_des_tcs.html', context)



@login_required(login_url='login')
@user_passes_test(lambda u: u.groups.filter(name='REPORTING').exists(),login_url='access_denied')
def info_tc(request) : 

    context = {

    }

    return render(request, 'reporting/info_tc.html', context)