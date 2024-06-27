from rest_framework import generics
from .models import SupportRequest
from .serializers import SupportRequestSerializer

class SupportRequestCreateView(generics.CreateAPIView):
    queryset = SupportRequest.objects.all()
    serializer_class = SupportRequestSerializer
