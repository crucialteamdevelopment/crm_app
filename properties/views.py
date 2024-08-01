from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from .models import Property, PropertyType, PropertyUnit, PropertyImage
from .serializers import PropertySerializer, CreatePropertySerializer, PropertyTypeSerializer, PropertyUnitSerializer, PropertyImageSerializer

class PropertyListCreateView(generics.ListCreateAPIView):
    queryset = Property.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreatePropertySerializer
        return PropertySerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PropertyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class PropertyImageListCreateView(generics.ListCreateAPIView):
    queryset = PropertyImage.objects.all()
    serializer_class = PropertyImageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        property_id = self.kwargs.get('property_id')
        return PropertyImage.objects.filter(property_id=property_id)

    def perform_create(self, serializer):
        property_id = self.kwargs.get('property_id')
        property = get_object_or_404(Property, pk=property_id)
        serializer.save(property=property)


class PropertyImageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PropertyImage.objects.all()
    serializer_class = PropertyImageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class PropertyTypeListView(generics.ListCreateAPIView):
    queryset = PropertyType.objects.all()
    serializer_class = PropertyTypeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class PropertyUnitListView(generics.ListCreateAPIView):
    queryset = PropertyUnit.objects.all()
    serializer_class = PropertyUnitSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class PropertyUnitDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PropertyUnit.objects.all()
    serializer_class = PropertyUnitSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
