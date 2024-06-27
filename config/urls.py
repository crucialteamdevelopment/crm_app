from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from users.views import LoginView, CustomTokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('api.urls')),
    path('api/properties/', include('properties.urls')),  # Добавляем маршруты приложения properties
    path('api/support/', include('support.urls')),
    
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)