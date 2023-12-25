
from io import BytesIO
import django_filters
from django.db import models
from django.http import HttpResponse
from django.template.loader import get_template
 
#pisa is a html2pdf converter using the ReportLab Toolkit,
#the HTML5lib and pyPdf.
 
from xhtml2pdf import pisa  
#difine render_to_pdf() function
 
def render_to_pdf(template_src, context_dict={}):
     template = get_template(template_src)
     html  = template.render(context_dict)
     result = BytesIO()
 
     #This part will create the pdf.
     pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result, debug=True)
     if not pdf.err:
         return HttpResponse(result.getvalue(), content_type='application/pdf')
     return None


def generate_filter_set(selected_model):

    class DynamicFilterSetMeta(django_filters.filterset.FilterSetMetaclass):
        def __new__(cls, name, bases, attrs, **kwargs):
            new_class = super().__new__(cls, name, bases, attrs, **kwargs)

            # Add methods to handle the "in" lookup for related model ids dynamically
            for field in new_class.base_filters.values():
                if isinstance(field, django_filters.filters.BaseInFilter):
                    related_model = field.field.related_model
                    method_name = f'filter_{related_model.__name__.lower()}_ids'

                    def filter_related_model_ids(queryset, name, value, related_model=related_model):
                        return queryset.filter(**{f'{name}__id__in': value})


                    # Attach the "in" lookup handler to the DynamicFilterSet
                    setattr(new_class, method_name, filter_related_model_ids)

            return new_class
    
    class DynamicFilterSet(django_filters.FilterSet,metaclass=DynamicFilterSetMeta):
        class Meta:
            model = selected_model
            fields = []


    def add_filters(selected_model, prefix='', processed_models=None):
        
        if processed_models is None:
            processed_models = set()

        if selected_model in processed_models:
            return

        processed_models.add(selected_model)

        for field in selected_model._meta.fields:
            filter_name = f'{prefix}{field.name}'
            if isinstance(field, models.ForeignKey):
                # Recursive call for related fields
                add_filters(field.related_model, f'{filter_name}__',processed_models)
                # Add an "in" lookup for related model ids
                DynamicFilterSet.base_filters[f'{filter_name}__in'] = django_filters.BaseInFilter(
                    field_name=f'{filter_name}__id',
                    lookup_expr='in',
                )
            else:
                if isinstance(field, models.CharField):
                    DynamicFilterSet.base_filters[filter_name + '__icontains'] = django_filters.CharFilter(
                        field_name=filter_name, lookup_expr='icontains'
                    )
                    DynamicFilterSet.base_filters[filter_name + '__exact'] = django_filters.CharFilter(
                        field_name=filter_name, lookup_expr='exact'
                    )

                elif isinstance(field, models.FloatField) or isinstance(field, models.DecimalField) or isinstance(field, models.IntegerField):
                    DynamicFilterSet.base_filters[filter_name] = django_filters.NumberFilter(
                        field_name=filter_name, lookup_expr='exact'
                    )
                    # Support for inexact lookups
                    DynamicFilterSet.base_filters[f'{filter_name}__gt'] = django_filters.NumberFilter(
                        field_name=filter_name, lookup_expr='gt'
                    )
                    DynamicFilterSet.base_filters[f'{filter_name}__lt'] = django_filters.NumberFilter(
                        field_name=filter_name, lookup_expr='lt'
                    )
                    DynamicFilterSet.base_filters[f'{filter_name}__gte'] = django_filters.NumberFilter(
                        field_name=filter_name, lookup_expr='gte'
                    )
                    DynamicFilterSet.base_filters[f'{filter_name}__lte'] = django_filters.NumberFilter(
                        field_name=filter_name, lookup_expr='lte'
                    )

                elif isinstance(field, models.DateField):
                    DynamicFilterSet.base_filters[filter_name] = django_filters.DateFilter(
                        field_name=filter_name, lookup_expr='exact'
                    )
                    # Support for inexact lookups
                    DynamicFilterSet.base_filters[f'{filter_name}__gt'] = django_filters.DateFilter(
                        field_name=filter_name, lookup_expr='gt'
                    )
                    DynamicFilterSet.base_filters[f'{filter_name}__lt'] = django_filters.DateFilter(
                        field_name=filter_name, lookup_expr='lt'
                    )
                    DynamicFilterSet.base_filters[f'{filter_name}__gte'] = django_filters.DateFilter(
                        field_name=filter_name, lookup_expr='gte'
                    )
                    DynamicFilterSet.base_filters[f'{filter_name}__lte'] = django_filters.DateFilter(
                        field_name=filter_name, lookup_expr='lte'
                    )

                elif isinstance(field, models.BooleanField):
                    DynamicFilterSet.base_filters[filter_name] = django_filters.BooleanFilter(
                        field_name=filter_name
                    )
                else:
                    DynamicFilterSet.base_filters[filter_name] = django_filters.CharFilter(
                        field_name=filter_name, lookup_expr='icontains'
                    )
                    DynamicFilterSet.base_filters[filter_name] = django_filters.CharFilter(
                        field_name=filter_name, lookup_expr='exact'
                    )                   
  
    add_filters(selected_model)


    return DynamicFilterSet