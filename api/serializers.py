from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from users.models import CustomUser

from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

    
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = (
            'username', 'password', 'password2', 'email', 'first_name', 'last_name', 
            'user_type', 'phone_number', 'company_name', 'company_type', 'role_in_company', 'tenant_type', 'tenant_subtype',
            'lender_type', 'service_type', 'industry', 'mailing_address', 'headquarters', 'established'
        )
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'email': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        if attrs['user_type'] == 'lender' and not attrs.get('lender_type'):
            raise serializers.ValidationError({"lender_type": "This field is required when user_type is 'lender'."})

        if attrs['user_type'] == 'tenant' and not attrs.get('headquarters'):
            raise serializers.ValidationError({"headquarters": "This field is required when user_type is 'tenant'."})

        if attrs['user_type'] == 'tenant' and not attrs.get('established'):
            raise serializers.ValidationError({"established": "This field is required when user_type is 'tenant'."})

        if attrs['user_type'] == 'tenant' and not attrs.get('tenant_type'):
            raise serializers.ValidationError({"tenant_type": "This field is required when user_type is 'tenant'."})
        
        if attrs['user_type'] == 'tenant' and not attrs.get('tenant_subtype'):
            raise serializers.ValidationError({"tenant_subtype": "This field is required when user_type is 'tenant'."})
        
        if attrs['user_type'] == 'tenant' and attrs['tenant_type'] == 'commercial':
            attrs['first_name'] = ''
            attrs['last_name'] = ''
        
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            user_type=validated_data['user_type'],
            phone_number=validated_data.get('phone_number', ''),
            company_name=validated_data.get('company_name', ''),
            company_type=validated_data.get('company_type', ''),
            role_in_company=validated_data.get('role_in_company', ''),
            service_type=validated_data.get('service_type', ''),
            industry=validated_data.get('industry', ''),
            lender_type=validated_data.get('lender_type', ''),
            tenant_type=validated_data.get('tenant_type', ''),
            tenant_subtype=validated_data.get('tenant_subtype', ''),
            mailing_address=validated_data.get('mailing_address', ''),
            headquarters=validated_data.get('headquarters', ''),
            established=validated_data.get('established', ''),
            password=validated_data['password']  # Используйте create_user для создания пользователя с паролем
        )
        return user
    
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

class SetNewPasswordSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)
    new_password2 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})
        return attrs

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'user_type')


