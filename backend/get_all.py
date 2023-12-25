import os 
import django
from django.apps import apps
import re
from django.db.models import ForeignKey,ManyToOneRel
from django.db import models

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")  
django.setup()

installed_apps = list(apps.get_app_configs())
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ONE_SPACE = "    "

def indent(spaces_number):
    if spaces_number < 0:
        raise ValueError("Number of spaces must be non-negative.")

    return ONE_SPACE * spaces_number

def createFile(app_path,app_name,file_name,premissions): 
    file_path = os.path.join(app_path,file_name)
    if not os.path.exists(file_path):
        with open(file_path, premissions) as created_file:
                created_file.write(f"# Your {file_name} code goes here\n")
        print(f"\n'{file_name}' file created in the selected app '{app_name}'.")

    else:
        print(f"\n'{file_name}' file already exists in the selected app '{app_name}'.")     

def addLine(file_path,line):     
    with open(file_path, 'a') as file:
        file.write(line + '\n')       

def addLineTop(file_path,line):     

    with open(file_path, 'r') as file:
        content = file.read()

    with open(file_path, 'w') as file:
        file.write(line + '\n')
        
        file.write(content) 

def getChoosedApps(installed_apps, input_message): 
    selected_apps = []

    printInstalledApps(installed_apps)

    user_input = input("\n"+input_message).lower()

    if user_input != 'done':
        try:
            selected_app_indices = [int(index) - 1 for index in user_input.split(',')]
            valid_indices = [index for index in selected_app_indices if 0 <= index < len(installed_apps)]

            for selected_index in valid_indices:
                selected_app_config = installed_apps[selected_index]
                selected_apps.append(selected_app_config)

            if not valid_indices:
                print("No valid selections. Please enter valid app numbers.")

        except ValueError:
            print("Invalid input. Please enter valid app numbers.")
    
    return selected_apps

def relatedFieldsCount(fields):
    count = 0
    for field in fields :
        if field.is_relation and isinstance(field, ForeignKey): 
            count  += 1

    return count 

def createModelSerializers(selected_app): 
    app_name = selected_app.name
    app_path = selected_app.path
    file_path = os.path.join(app_path,'generated_serializers.py')

    #Check if there is a serialzers file on  the selected apps and create one if there is not
    createFile(app_path,app_name,'generated_serializers.py',"w")

    addLine(file_path,f"from rest_framework import serializers")
    addLine(file_path,f"from .models import *")
    addLine(file_path,f"from rest_flex_fields import FlexFieldsModelSerializer")
    addLine(file_path,f"from drf_writable_nested.serializers import WritableNestedModelSerializer")
        
    filtered_models = [model for model in selected_app.get_models() if len(model.__bases__) == 1]
    
    for model in filtered_models:
        for field in model._meta.get_fields():
            if hasattr(field, 'related_name') and field.related_name:
                related_model = field.related_model 
                forign = True 
                for elem in selected_app.get_models(): 
                    if elem.__name__ == related_model.__name__: 
                        forign = False 
                        
                if forign: 
                    addLine(file_path,f"from {related_model._meta.app_label}.serializers import *")  

    addLine(file_path,f"\n")


    models = [model for model in selected_app.get_models() if len(model.__bases__) == 1]

    sorted_models = []
    for model in models:
        has = False 
        for field in model._meta.get_fields():
            if hasattr(field, 'related_name') and field.related_name:
                has = True 
        if has: 
            sorted_models.append(model)
        else:
            sorted_models.insert(0,model) 
                
    for model in sorted_models:
        model_name = model.__name__ 
        print(f'Creating the {model_name} serializer...')

        addLine(file_path,f"class {model_name}Serializer(FlexFieldsModelSerializer,WritableNestedModelSerializer):")

        for field in model._meta.get_fields():
            if hasattr(field, 'related_name') and field.related_name:
                addLine(file_path,f"{indent(1)}{field.name} = {field.related_model.__name__}Serializer(many=True,required=False)")


        addLine(file_path,f"{indent(1)}class Meta:")
        addLine(file_path,f"{indent(2)}model = {model_name}")
        addLine(file_path,f"{indent(2)}fields = '__all__'")
        addLine(file_path,"\n")
        fields = model._meta.get_fields()
        if relatedFieldsCount(fields) > 0:
            addLine(file_path,f"{indent(2)}expandable_fields = "+"{")
            for field in fields :
                if field.is_relation and isinstance(field, ForeignKey):                       
                    addLine(file_path,f"{indent(3)}'{field.name}': ('{field.related_model._meta.app_label}.serializers.{field.related_model.__name__}Serializer',"+ "{'many': False}),")

                if field.is_relation and isinstance(field, ManyToOneRel): 


                    related_field_name = field.name 
                    if field.related_name is None: 
                        related_field_name = field.name.lower()+"s"
                    addLine(file_path,f"{indent(3)}'{related_field_name}': ('{field.related_model._meta.app_label}.serializers.{field.related_model.__name__}Serializer',"+ "{'many': True}),")            
                    
            addLine(file_path,f"{indent(3)} "+"}")
            addLine(file_path,"\n")

def is_numeric_field(field):
    numeric_field_types = [
        models.DecimalField,
        models.FloatField,
        models.IntegerField,
        models.PositiveIntegerField,
        models.PositiveSmallIntegerField,
        models.SmallIntegerField,
    ]

    return any(isinstance(field, field_type) for field_type in numeric_field_types)

def getUserApps(all_apps,BASE_DIR): 
    installed = [] 
    for i, app in enumerate(all_apps, start=1):
        if f"{BASE_DIR}\{app.name}" == app.path:
            installed.append(app)
   
    return installed 

def printInstalledApps(apps): 

    print("\n"+"Installed Apps:")
    index = 1

    for item in apps:
        print(f"{index}. {item.name}")
        index = index + 1
    print(f"{index}. All")

def clearFile(file_path,app_name): 
    try:
        # Open the file in write mode, which truncates the file and removes all data
        with open(file_path, 'w') as file:
            print(f'{app_name} -> All data removed from {file_path}')
    except Exception as e:
        print(f'An error occurred: {e}')


def customUpdate(model,one2ManyFields,many2OneFields,file_path):

    addLine(file_path, f"{indent(1)}def update(self, request, *args, **kwargs):")
    addLine(file_path,f"{indent(2)}partial = kwargs.pop('partial', False)")
    addLine(file_path,f"{indent(2)}instance = self.get_object()")
    addLine(file_path,f"\n")

    for _field in one2ManyFields: 
        addLine(file_path,f"{indent(2)}# Update nested { _field.name }")
        addLine(file_path,f"{indent(2)}{_field.name}_data = request.data.pop('{_field.name}', None)")
        addLine(file_path,f"{indent(2)}if isinstance({_field.name}_data, int):")
        addLine(file_path,f"{indent(3)}request.data['{_field.name}'] = {_field.name}_data")
        addLine(file_path,f"{indent(2)}elif {_field.name}_data:")
        addLine(file_path,f"{indent(3)}{_field.name}_id = {_field.name}_data.get('id')")
        addLine(file_path,f"{indent(3)}if {_field.name}_id:")

        addLine(file_path,f"{indent(4)}# If 'id' is present, it's an update")
        addLine(file_path,f"{indent(4)}{_field.name}_instance = {_field.related_model.__name__}.objects.get(id={_field.name}_id)")
        addLine(file_path,f"{indent(4)}{_field.name}_serializer = {_field.related_model.__name__}Serializer({_field.name}_instance,data={_field.name}_data, partial=partial)")
        addLine(file_path,f"{indent(4)}{_field.name}_serializer.is_valid(raise_exception=True)")
        addLine(file_path,f"{indent(4)}{_field.name}_serializer.save()")
        addLine(file_path,f"{indent(3)}else:")
        addLine(file_path,f"{indent(4)}# If 'id' is not present, it's a create")
        addLine(file_path,f"{indent(4)}{_field.name}_serializer = {_field.related_model.__name__}Serializer(data={_field.name}_data)")
        addLine(file_path,f"{indent(4)}{_field.name}_serializer.is_valid(raise_exception=True)")
        addLine(file_path,f"{indent(4)}{_field.name} = {_field.name}_serializer.save()")
        addLine(file_path,f"{indent(4)}request.data['{_field.name}'] = {_field.name}.id")
        addLine(file_path,f"\n")
        
    addLine(file_path,f"{indent(2)}{model.__name__.lower()}_serializer = self.get_serializer(instance,data=request.data, partial=partial)")
    addLine(file_path,f"{indent(2)}{model.__name__.lower()}_serializer.is_valid(raise_exception=True)")
    addLine(file_path,f"{indent(2)}{model.__name__.lower()}_instance = {model.__name__.lower()}_serializer.save()")
    addLine(file_path,f"\n")

    for __field in many2OneFields: 
        related_name = __field.related_name 
        related_name_single = __field.related_model.__name__.lower() 
        related_model_name = __field.related_model.__name__ 
        addLine(file_path,f"{indent(2)}# Update nested { related_name } ")
        addLine(file_path,f"{indent(2)}{related_name}_data = request.data.pop('{related_name}', [])")
        addLine(file_path,f"{indent(2)}if {related_name}_data:")
        addLine(file_path,f"{indent(3)}for {related_name_single}_data in {related_name}_data:")
        addLine(file_path,f"{indent(4)}if isinstance({related_name_single}_data, int):")
        addLine(file_path,f"{indent(5)}pass")
        addLine(file_path,f"{indent(4)}else: ")
        addLine(file_path,f"{indent(5)}{related_name_single}_id = {related_name}_data.get('id')")
        addLine(file_path,f"{indent(5)}if {related_name_single}_id:")
        addLine(file_path,f"{indent(6)}# If 'id' is present, it's an update")
        addLine(file_path,f"{indent(6)}{related_name}_instance = {related_model_name}.objects.get(id={related_name_single}_id)")
        addLine(file_path,f"{indent(6)}{related_name}_serializer = {related_model_name}Serializer({related_name}_instance, data={related_name}_data, partial=partial)")
        addLine(file_path,f"{indent(5)}else:")
        addLine(file_path,f"{indent(6)}# If 'id' is not present, it's a create")
        addLine(file_path,f"{indent(6)}{related_name}_data['{model.__name__.lower()}'] = {model.__name__.lower()}_instance.id")
        addLine(file_path,f"{indent(6)}{related_name}_serializer = {related_model_name}Serializer(data={related_name}_data)")
        addLine(file_path,f"{indent(5)}{related_name}_serializer.is_valid(raise_exception=True)")
        addLine(file_path,f"{indent(5)}{related_name}_serializer.save()")
    
    addLine(file_path,f"{indent(2)}return Response({model.__name__.lower()}_serializer.data)")







    addLine(file_path, f"\n") 


def customCreate(model,one2ManyFields,many2OneFields,file_path): 

    addLine(file_path, f"{indent(1)}def create(self, request, *args, **kwargs):")

    for field in many2OneFields: 
        addLine(file_path,f"{indent(2)}{field.related_name}_data = request.data.pop('{field.related_name}',[])")

    for _field in one2ManyFields: 
        addLine(file_path,f"{indent(2)}# Create nested { _field.name } ")
        addLine(file_path,f"{indent(2)}{_field.name}_data = request.data.get('{_field.name}')")
        addLine(file_path,f"{indent(2)}if isinstance({_field.name}_data, int):")
        addLine(file_path,f"{indent(3)}request.data['{_field.name}'] = {_field.name}_data")
        addLine(file_path,f"{indent(2)}elif {_field.name}_data:")
        addLine(file_path,f"{indent(3)}{_field.name}_serializer = {_field.related_model.__name__}Serializer(data={_field.name}_data)")
        addLine(file_path,f"{indent(3)}if {_field.name}_serializer.is_valid():")
        addLine(file_path,f"{indent(4)}{_field.name} = {_field.name}_serializer.save()")
        addLine(file_path,f"{indent(4)}request.data['{_field.name}'] = {_field.name}.id")
        addLine(file_path,f"{indent(3)}else:")
        addLine(file_path,f"{indent(4)}return Response({_field.name}_serializer.errors, status=status.HTTP_400_BAD_REQUEST)")
        addLine(file_path,f"\n")
        
    addLine(file_path,f"{indent(2)}{model.__name__.lower()}_serializer = self.get_serializer(data=request.data)")
    addLine(file_path,f"{indent(2)}{model.__name__.lower()}_serializer.is_valid(raise_exception=True)")
    addLine(file_path,f"{indent(2)}{model.__name__.lower()}_instance = {model.__name__.lower()}_serializer.save()")
    addLine(file_path,f"\n")

    for __field in many2OneFields: 
        addLine(file_path,f"{indent(2)}# Create nested { field.related_name }")
        addLine(file_path,f"\n")
        addLine(file_path,f"{indent(2)}for {__field.related_model.__name__.lower()}_data in {__field.related_name}_data:")
        addLine(file_path,f"{indent(3)}{__field.related_model.__name__.lower()}_data['{model.__name__.lower()}'] = {model.__name__.lower()}_instance.id")
        addLine(file_path,f"{indent(3)}{__field.related_model.__name__.lower()}_serializer = {__field.related_model.__name__}Serializer(data={__field.related_model.__name__.lower()}_data)")
        addLine(file_path,f"{indent(3)}{__field.related_model.__name__.lower()}_serializer.is_valid(raise_exception=True)")
        addLine(file_path,f"{indent(3)}{__field.related_model.__name__.lower()}_serializer.save()")
        addLine(file_path,f"\n")

    addLine(file_path,f"{indent(2)}headers = self.get_success_headers({model.__name__.lower()}_serializer.data)")
    addLine(file_path,f"{indent(2)}return Response({model.__name__.lower()}_serializer.data, status=201, headers=headers)")


    addLine(file_path, f"\n") 

def RelatedModelSchema(related_field, schema): 
    related_model = related_field.related_model

    fields = related_model._meta.get_fields() 
    for field in fields: 
        if isinstance(field, models.ForeignKey): 
            schema.append({
                'title' : field.name, 
                'children': schema.append(RelatedModelSchema(field,schema))
            })
            
        elif isinstance(field, models.OneToOneRel) or isinstance(field, models.ManyToOneRel):
            continue
        else:
            item = {
                'title' : field.name
            }
            schema.append(item)

    return schema

def modelSchema(model): 

    fields = model._meta.get_fields()
    schema = []  
    for field in fields: 
        if isinstance(field, models.ForeignKey): 
            item = {
                'title' : field.name
            }
            schema.append(RelatedModelSchema(field,schema))
        elif isinstance(field, models.OneToOneRel) or isinstance(field, models.ManyToOneRel):
            continue
        else:
            item = {
                'title' : field.name
            }
            schema.append(item)
    
    print(schema)

def createSchema(model,file_path,schema=None,processed_fields=None,parent_field=None,parent=None): 
    
    modelSchema(model)

    if processed_fields is None:
        processed_fields = set()

    if schema is None:
        schema = []

   
    _fields = model._meta.get_fields()
    fields = [field for field in _fields if field.name != 'id']
    for field in fields: 
        if field in processed_fields: 
            continue

        processed_fields.add(field)

        if field.is_relation and isinstance(field, models.ForeignKey): 
            if parent_field is None: 
                schema = []
            related_model = field.related_model
            schema.append(field.name)
            createSchema(related_model,file_path,schema,processed_fields, parent_field=field.name,parent=field) 
               
        elif field.is_relation and isinstance(field, ManyToOneRel): 
            continue 
        else: 
        

             
            #render: (record:any) => record.raison_sociale,
            if parent_field is None: 
                schema = []
            schema.append(field.name)

            addLine(file_path,"    {")
            addLine(file_path,f'{indent(2)}title:"{field.verbose_name.lower().capitalize()}",')

            if parent_field:
                addLine(file_path,f'{indent(2)}dataIndex:"{schema[0]}",')
            else: 
                addLine(file_path,f'{indent(2)}dataIndex:"{field.name}",')

            addLine(file_path,f'{indent(2)}schema:{schema},')
           

            if len(schema) == 1 :
                addLine(file_path,f'{indent(2)}key:"{field.name}",')
                addLine(file_path,f'{indent(2)}render: (record:any) => record,')

            else:
                render_schema = schema[:]
                render_schema.pop(0)
                addLine(file_path,f'{indent(2)}render: (record:any) => record?.{'?.'.join(render_schema)},')
                addLine(file_path,f'{indent(2)}key:"{'_'.join(schema)}",')

            if len(schema) > 1 :
                addLine(file_path,f'{indent(2)}expand:"{'.'.join(schema)}",')

            if len(schema) == 1 :
                addLine(file_path,f'{indent(2)}checked:true,')
            else:
                addLine(file_path,f'{indent(2)}checked:false,')

            addLine(file_path,f'{indent(2)}width:150,')
            addLine(file_path,f'{indent(2)}ellipsis: true,')

            addLine(file_path,"    },")




        schema.pop() 

            
def createData(selected_app):
    createFile(selected_app.path,app_name,'data.ts',"w")
    file_path = os.path.join(selected_app.path,'data.ts')

    models =  [model for model in selected_app.get_models() if len(model.__bases__) == 1]
    for model in models: 
        addLine(file_path,f"export const {model.__name__.upper()}_COLUMNS = [")
        createSchema(model,file_path,schema=None,processed_fields=None)
   
        addLine(file_path,f"];")
        addLine(file_path,f"\n")

def createViews(selected_app): 

    app_name = selected_app.name

    createFile(selected_app.path,app_name,'generated_views.py',"w")
    file_path = os.path.join(selected_app.path,'generated_views.py')

    addLine(file_path,f"from rest_framework.response import Response")
    addLine(file_path,f"from rest_framework import viewsets,filters,status")
    addLine(file_path,f"from rest_framework.decorators import action") 
    addLine(file_path,f"from rest_framework.pagination import PageNumberPagination") 
    addLine(file_path,f"from .models import *") 
    addLine(file_path,f"from .filters import *") 
    addLine(file_path,f"from django_filters.rest_framework import DjangoFilterBackend")
    addLine(file_path,f"from rest_flex_fields import is_expanded")

    for item in selected_apps_to_explore:
        if item == selected_app: 
            pass
        else:  
            addLine(file_path,f"from {item.name}.serializers import *") 
                
    addLine(file_path,"\n") 
    addLine(file_path,f"class CustomPagination(PageNumberPagination):") 
    addLine(file_path,f"{indent(1)}page_size = 10") 
    addLine(file_path,f"{indent(1)}page_size_query_param = 'page_size'") 
    addLine(file_path,f"{indent(1)}max_page_size = 10000") 

    addLine(file_path,"\n") 
    
   

    models =  [model for model in selected_app.get_models() if len(model.__bases__) == 1]
    for model in models:

        addLine(file_path, f"class {model.__name__}ViewSet(viewsets.ModelViewSet):")
        addLine(file_path, f"{indent(1)}queryset = {model.__name__}.objects.all()")
        addLine(file_path, f"{indent(1)}filter_backends = [DjangoFilterBackend,filters.OrderingFilter]")
        addLine(file_path, f"{indent(1)}serializer_class = {model.__name__}Serializer")
        addLine(file_path, f"{indent(1)}pagination_class = CustomPagination")
        addLine(file_path, f"{indent(1)}ordering_fields = '__all__'")
        addLine(file_path, f"{indent(1)}filterset_class= {model.__name__}Filter")
        addLine(file_path, f"\n")


        fields = model._meta.get_fields()
        one2ManyFields = []
        many2OneFields = []

        if relatedFieldsCount(fields) > 0:
            for field in fields :
                if field.is_relation and isinstance(field, ForeignKey):   
                    one2ManyFields.append(field) # Like Regime in Gros - A single object

                if field.is_relation and isinstance(field, ManyToOneRel): 
                    if field.related_name is not None:
                        many2OneFields.append(field) # Like Articles in Gros - A list of objects
                
        customCreate(model,one2ManyFields,many2OneFields,file_path)
        customUpdate(model,one2ManyFields,many2OneFields,file_path)

        expandable_fields = model._meta.get_fields()
        if relatedFieldsCount(expandable_fields) > 0:

            addLine(file_path, f"{indent(1)}def get_queryset(self):")
            addLine(file_path, f"{indent(2)}queryset = {model.__name__}.objects.all()")

            for expandable_field in expandable_fields :
                if expandable_field.is_relation and isinstance(expandable_field, ForeignKey):     
                    addLine(file_path, f"{indent(2)}if is_expanded(self.request, '{expandable_field.name}'):")
                    addLine(file_path, f"{indent(3)}queryset = queryset.prefetch_related('{expandable_field.name}')")
            
            addLine(file_path, f"{indent(2)}return queryset")
            addLine(file_path, f"\n")

        addLine(file_path, f"{indent(1)}def list(self, request, *args, **kwargs):")
        addLine(file_path, f"{indent(2)}# Check if the 'all' parameter is present in the request query parameters")
        addLine(file_path, f"{indent(2)}if request.query_params.get('all', False):")
        addLine(file_path, f"{indent(3)}# If 'all' is present, return all records without pagination")
        addLine(file_path, f"{indent(3)}queryset = self.filter_queryset(self.get_queryset())")
        addLine(file_path, f"{indent(3)}serializer = self.get_serializer(queryset, many=True)")
        addLine(file_path, f"{indent(3)}return Response(serializer.data)")
        addLine(file_path, f"{indent(2)}# If 'all' is not present, proceed with pagination as usual")
        addLine(file_path, f"{indent(2)}return super().list(request, *args, **kwargs)")
        addLine(file_path, f"\n")

        # Handle bulk deletion 
        addLine(file_path, f"{indent(1)}@action(detail=False, methods=['post'])")
        addLine(file_path, f"{indent(1)}def bulk_delete(self, request, *args, **kwargs):")

        addLine(file_path, f"{indent(2)}ids = request.data.get('ids', [])")
        addLine(file_path, f"{indent(2)}if not ids:")
        addLine(file_path, "           return Response({'detail': 'No IDs provided for deletion.'}, status=status.HTTP_400_BAD_REQUEST)")

        addLine(file_path, f"{indent(2)}try:")
        addLine(file_path, f"{indent(3)}queryset = self.filter_queryset(self.get_queryset())")
        addLine(file_path, f"{indent(3)}deleted, _ = queryset.filter(pk__in=ids).delete()")
        addLine(file_path, f"{indent(3)}if deleted > 0:")
        addLine(file_path, "               return Response({'detail': f'Successfully deleted objects with ids: {ids} .'}, status=status.HTTP_204_NO_CONTENT)")
        addLine(file_path, f"{indent(3)}else:")
        addLine(file_path, "               return Response({'detail': 'No objects found for deletion.'}, status=status.HTTP_404_NOT_FOUND)")
        addLine(file_path, f"{indent(2)}except Exception as e:")
        addLine(file_path, "           return Response({'detail': f'Error during deletion: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)")
        addLine(file_path, "\n")

def createUrls(app): 
    app_models = app.get_models()
    file_path = os.path.join(app.path,'generated_urls.py')
    addLineTop(file_path,"from .views import *")
    addLineTop(file_path,"from rest_framework import routers")
    addLine(file_path,f"app_name='{app.name}'")
    addLine(file_path,"\n")
    addLine(file_path,"router = routers.DefaultRouter()")
    addLine(file_path,"\n")

    urlpatterns = False
    with open(file_path, 'r') as file:

        for line in file:

            if 'urlpatterns' in line:
                urlpatterns = True
                break 
    
    if not urlpatterns: 
        addLine(file_path,"urlpatterns = []")
        addLine(file_path,"\n")

    models = [model for model in selected_app.get_models() if len(model.__bases__) == 1]

    for item in models: 
        addLine(file_path,f"router.register(r'{item.__name__.lower()}', {item.__name__}ViewSet, basename='{item.__name__.lower()}')")
    addLine(file_path,"urlpatterns += router.urls")

def createFilter(selected_app):
    app_name = selected_app.name
    app_path = selected_app.path
    #Get the erializers file path for the selected app 
    filters_file_path = os.path.join(app_path,'generated_filters.py')

    #Check if there is a serialzers file on  the selected apps and create one if there is not
    createFile(app_path,app_name,'generated_filters.py',"w")
    addLine(filters_file_path,f"from .models import *")
    addLine(filters_file_path,f"from .serializers import *")
    addLine(filters_file_path,f"from src.utils import generate_filter_set ") 
    addLine(filters_file_path,"\n") 


    models = [model for model in selected_app.get_models() if len(model.__bases__) == 1]
    for model in models:
        addLine(filters_file_path,f"{model.__name__}Filter = generate_filter_set({model.__name__})") 


def clearFiles(user_apps): 

    selected_apps_to_clear = getChoosedApps(user_apps,"Enter the numbers of apps you want to empty (comma-separated): ")

    print("\n"+"Selected apps: ",", ".join(app.name for app in selected_apps_to_clear))

    user_input = input("\n"+"Are you sure you want to clear the serializers and filters ? type 'clear': ").lower()

    if user_input == "clear": 
        for selected_app in selected_apps_to_clear: 
            app_name = selected_app.name
            app_path = selected_app.path

            file_path = os.path.join(app_path,'generated_serializers.py')
            clearFile(file_path, app_name)

            file_path = os.path.join(app_path,'generated_filters.py')
            clearFile(file_path, app_name)

            file_path = os.path.join(app_path,'generated_views.py')
            clearFile(file_path, app_name)

            file_path = os.path.join(app_path,'generated_urls.py')
            clearFile(file_path, app_name)

            file_path = os.path.join(app_path,'data.ts')
            clearFile(file_path, app_name)





try:
    user_apps = getUserApps(installed_apps,BASE_DIR)
    # Prompt the user to input the app name
    selected_apps_to_explore = getChoosedApps(user_apps,"Enter the numbers of apps you want to generate (comma-separated):")
    
    clearFiles(user_apps)

    for selected_app in selected_apps_to_explore: 
        app_name = selected_app.name
        app_path = selected_app.path

        createUrls(selected_app)
        createModelSerializers(selected_app)  
        createViews(selected_app)  
        createFilter(selected_app)
        createData(selected_app)


except IndexError:
    print("Invalid input.")
except Exception as e:
    print(f"An error occurred: {e}")