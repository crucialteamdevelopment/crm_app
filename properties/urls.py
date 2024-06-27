from django.urls import path
from .views import PropertyListCreateView, PropertyDetailView,PropertyTypeListView,PropertyUnitListView, PropertyUnitDetailView, PropertyImageListCreateView, PropertyImageDetailView


urlpatterns = [
    path('', PropertyListCreateView.as_view(), name='property-list-create'),
    path('<int:pk>/', PropertyDetailView.as_view(), name='property-detail'),
    path('property-types/', PropertyTypeListView.as_view(), name='property-type-list-create'),
    path('property-units/', PropertyUnitListView.as_view(), name='property-unit-list-create'),
    path('property-units/<int:pk>/', PropertyUnitDetailView.as_view(), name='property-unit-detail'),
    path('<int:property_id>/images/', PropertyImageListCreateView.as_view(), name='property-image-list-create'),
    path('<int:property_id>/images/<int:pk>/', PropertyImageDetailView.as_view(), name='property-image-detail'),

]
