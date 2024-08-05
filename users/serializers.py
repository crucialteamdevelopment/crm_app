from rest_framework import serializers
from .models import CompanyType, RoleInCompany, Industry, ServiceType, TenantType, TenantSubtype, Company, PhoneNumber, Directory, UserFile, CustomUser



        
        
class CompanyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyType
        fields = '__all__'

class RoleInCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleInCompany
        fields = '__all__'

class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = '__all__'

class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = '__all__'

class TenantTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantType
        fields = '__all__'

class TenantSubtypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantSubtype
        fields = '__all__'


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password'] != data['new_password2']:
            raise serializers.ValidationError({"new_password": "New passwords must match."})
        return data
    
    


class CompanySerializer(serializers.ModelSerializer):
    company_type = serializers.CharField()

    class Meta:
        model = Company
        fields = ['id', 'name', 'about', 'company_type']

    def create(self, validated_data):
        company_type_name = validated_data.pop('company_type')
        company_type, created = CompanyType.objects.get_or_create(name=company_type_name)
        company = Company.objects.create(company_type=company_type, **validated_data)
        return company

    def update(self, instance, validated_data):
        if 'company_type' in validated_data:
            company_type_name = validated_data.pop('company_type')
            company_type, created = CompanyType.objects.get_or_create(name=company_type_name)
            instance.company_type = company_type
        return super().update(instance, validated_data)
    
    
class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = ['id', 'number', 'title']
        
              
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
        
        
class CustomUserSerializer(serializers.ModelSerializer):
    companies = CompanySerializer(many=True, read_only=True)
    phone_numbers = PhoneNumberSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'first_name', 'last_name', 
            'is_superuser', 'is_staff', 'is_active', 'date_joined',
            'user_type', 'email', 'phone_number', 'company_name',
            'lender_type', 'headquarters', 'established', 'mailing_address',
            'company_type', 'role_in_company', 'industry', 'service_type',
            'tenant_type', 'tenant_subtype', 'companies', 'phone_numbers'
        ]
