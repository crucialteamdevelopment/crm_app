from django.urls import path
from .views import SupportRequestCreateView

urlpatterns = [
    path('', SupportRequestCreateView.as_view(), name='support-request-create'),
]
