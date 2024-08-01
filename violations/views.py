from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Violation, Field
from .serializers import ViolationSerializer, FieldSerializer

@api_view(['GET', 'POST'])
def violation_list(request):
    if request.method == 'GET':
        violations = Violation.objects.all()
        serializer = ViolationSerializer(violations, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ViolationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def field_list(request):
    if request.method == 'GET':
        fields = Field.objects.all()
        serializer = FieldSerializer(fields, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = FieldSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def violation_detail(request, pk):
    violation = get_object_or_404(Violation, pk=pk)
    if request.method == 'GET':
        serializer = ViolationSerializer(violation)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ViolationSerializer(violation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        violation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
