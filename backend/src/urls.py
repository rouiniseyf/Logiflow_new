from django.contrib import admin
from django.urls import path, include
from app.views.views import *
from billing.views import * 
from groupage.views import * 
import debug_toolbar

urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
    path("admin/", admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/auth/', include('authentication.urls')),
    path('api/container/', include('app.urls')),
    path('api/bareme/', include('bareme.urls')),
    path('api/billing/', include('billing.urls')),
    path('api/reposrting/', include('reporting.urls')),
    path('api/reference/', include('reference.urls')),
    path('api/groupage/', include('groupage.urls'))
]

