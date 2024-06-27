from rest_framework import serializers
from .models import SupportRequest

class SupportRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportRequest
        fields = ['id', 'name', 'email', 'message', 'created_at']
