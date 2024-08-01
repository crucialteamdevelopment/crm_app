from django.urls import path
from .views import violation_list, field_list, violation_detail

urlpatterns = [
    path('', violation_list, name='violation-list'),
    path('<int:pk>/', violation_detail, name='violation-detail'),
    path('fields/', field_list, name='field-list'),
]
