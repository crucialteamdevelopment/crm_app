from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
###
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

class TestView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Returns a simple status message",
        responses={200: "OK"},
    )
    def get(self, request):
        return Response({"status": "ok!"})
    
###

schema_view = get_schema_view(
    openapi.Info(
        title="CRM API",
        default_version='v1',
        description="CRM API docs",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@yourapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    url='https://crucial-development.pp.ua'
)

urlpatterns = [


    path('', TestView.as_view(), name='test-view'),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/properties/', include('properties.urls')), 
    path('api/support/', include('support.urls')),
    path('api/bookmarks/', include('bookmarks.urls')),
    path('api/violations/', include('violations.urls')),
    path('api/local_law/', include('local_law.urls')),
    
    path('api/users/', include('users.urls')),
    
    
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
