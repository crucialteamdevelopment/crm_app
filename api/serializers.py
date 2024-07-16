from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from users.models import CustomUser
from django.utils.translation import gettext_lazy as _

class CustomUniqueEmailValidator:
    def __call__(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already exists.", code='invalid')

class CustomValidationError(serializers.ValidationError):
    def __init__(self, detail):
        self.detail = {"error": detail}
        super().__init__(detail=self.detail)

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField()

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

        # Проверка уникальности email
        if CustomUser.objects.filter(email=attrs['email']).exists():
            raise CustomValidationError(detail="Email is already exists.")

        if attrs['user_type'] == 'lender' and not attrs.get('lender_type'):
            raise serializers.ValidationError({"lender_type": "This field is required when user_type is 'lender'."})

        if attrs['user_type'] == 'tenant' and attrs.get('tenant_subtype') == 'company' and not attrs.get('headquarters'):
            raise serializers.ValidationError({"headquarters": "This field is required when user_type is 'tenant' and tenant_subtype is 'company'."})

        if attrs['user_type'] == 'tenant' and attrs.get('tenant_type') == 'commercial' and not attrs.get('established'):
            raise serializers.ValidationError({"established": "This field is required when user_type is 'tenant' and tenant_type is 'commercial'."})

        if attrs['user_type'] == 'tenant' and not attrs.get('tenant_type'):
            raise serializers.ValidationError({"tenant_type": "This field is required when user_type is 'tenant'."})
        
        if attrs['user_type'] == 'tenant' and attrs.get('tenant_type') == 'commercial' and not attrs.get('tenant_subtype'):
            raise serializers.ValidationError({"tenant_subtype": "This field is required when user_type is 'tenant'."})
        
        if attrs['user_type'] == 'tenant' and attrs.get('tenant_type') == 'commercial':
            attrs['first_name'] = ''
            attrs['last_name'] = ''
        
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')  # Убираем поле password2, так как оно не нужно для создания пользователя
        password = validated_data.pop('password')

        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()

        return user

    def validate_email(self, value):
        validator = CustomUniqueEmailValidator()
        try:
            validator(value)
        except serializers.ValidationError as e:
            raise CustomValidationError(detail=str(e.detail[0]))

        return value

# Другие сериализаторы остаются без изменений
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
