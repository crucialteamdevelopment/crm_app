from rest_framework import serializers
from .models import Directory, UserFile
from .models import CustomUser, PhoneNumber, Company

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'user_type', 'company_name',
            'company_type', 'role_in_company', 'industry', 'service_type',
            'lender_type', 'headquarters', 'established', 'mailing_address',
            'tenant_type', 'tenant_subtype'
        )

        extra_kwargs = {
            'id': {'read_only': True},
        }


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password'] != data['new_password2']:
            raise serializers.ValidationError({"new_password": "New passwords must match."})
        return data
    
    
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'type', 'about']

class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = ['id', 'number']
        
              
class DirectorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Directory
        fields = ['id', 'user', 'name', 'parent_directory', 'created_at']
        read_only_fields = ['user', 'created_at']


class UserFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFile
        fields = ['id', 'user', 'directory', 'file', 'uploaded_at', 'file_type', 'tag', 'description']
        read_only_fields = ['user', 'uploaded_at']
