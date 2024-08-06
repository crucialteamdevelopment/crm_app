from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _

from users.models import CustomUser, CompanyType, RoleInCompany, Industry, ServiceType, TenantType, TenantSubtype, LenderType


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    company_type = serializers.SlugRelatedField(
        queryset=CompanyType.objects.all(),
        slug_field='name',
        required=False,
        allow_null=True
    )
    role_in_company = serializers.SlugRelatedField(
        queryset=RoleInCompany.objects.all(),
        slug_field='name',
        required=False,
        allow_null=True
    )
    industry = serializers.SlugRelatedField(
        queryset=Industry.objects.all(),
        slug_field='name',
        required=False,
        allow_null=True
    )
    service_type = serializers.SlugRelatedField(
        queryset=ServiceType.objects.all(),
        slug_field='name',
        required=False,
        allow_null=True
    )
    tenant_type = serializers.SlugRelatedField(
        queryset=TenantType.objects.all(),
        slug_field='name',
        required=False,
        allow_null=True
    )
    tenant_subtype = serializers.SlugRelatedField(
        queryset=TenantSubtype.objects.all(),
        slug_field='name',
        required=False,
        allow_null=True
    )
    lender_type = serializers.SlugRelatedField(
        queryset=LenderType.objects.all(),  # Убедитесь, что у вас есть модель LenderType
        slug_field='name',
        required=False,
        allow_null=True
    )

    class Meta:
        model = CustomUser
        fields = (
            'username', 'password', 'password2', 'email', 'first_name', 'last_name',
            'user_type', 'phone_number', 'company_name', 'company_type', 'role_in_company',
            'tenant_type', 'tenant_subtype', 'lender_type', 'service_type', 'industry',
            'mailing_address', 'headquarters', 'established'
        )
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'email': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": _("Password fields didn't match.")})

        user_type = attrs['user_type']
        tenant_type = attrs.get('tenant_type')
        tenant_subtype = attrs.get('tenant_subtype')

        if user_type == 'lender' and not attrs.get('lender_type'):
            raise serializers.ValidationError({"lender_type": _("This field is required when user_type is 'lender'.")})

        if user_type == 'tenant':
            if tenant_type == 'commercial':
                if not attrs.get('headquarters'):
                    raise serializers.ValidationError({"headquarters": _("This field is required when tenant_subtype is 'company'.")})
                if not attrs.get('established'):
                    raise serializers.ValidationError({"established": _("This field is required when tenant_subtype is 'company'.")})

            if tenant_type == 'residential' and tenant_subtype:
                pass

            if not tenant_type:
                raise serializers.ValidationError({"tenant_type": _("This field is required when user_type is 'tenant'.")})
            if tenant_type != 'residential' and not tenant_subtype:
                raise serializers.ValidationError({"tenant_subtype": _("This field is required when tenant_type is not 'residential'.")})

            if tenant_type == 'commercial':
                attrs['first_name'] = ''
                attrs['last_name'] = ''

        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')

        lender_type_name = validated_data.get('lender_type', None)
        if lender_type_name:
            lender_type, created = LenderType.objects.get_or_create(name=lender_type_name)
            validated_data['lender_type'] = lender_type

        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            user_type=validated_data['user_type'],
            phone_number=validated_data.get('phone_number', ''),
            company_name=validated_data.get('company_name', ''),
            company_type=validated_data.get('company_type', None),
            role_in_company=validated_data.get('role_in_company', None),
            service_type=validated_data.get('service_type', None),
            industry=validated_data.get('industry', None),
            lender_type=validated_data.get('lender_type', None),
            tenant_type=validated_data.get('tenant_type', None),
            tenant_subtype=validated_data.get('tenant_subtype', None),
            mailing_address=validated_data.get('mailing_address', ''),
            headquarters=validated_data.get('headquarters', ''),
            established=validated_data.get('established', ''),
            password=validated_data['password']
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
    company_type = serializers.CharField(source='company_type.name', read_only=True)
    role_in_company = serializers.CharField(source='role_in_company.name', read_only=True)
    industry = serializers.CharField(source='industry.name', read_only=True)
    service_type = serializers.CharField(source='service_type.name', read_only=True)
    tenant_type = serializers.CharField(source='tenant_type.name', read_only=True)
    tenant_subtype = serializers.CharField(source='tenant_subtype.name', read_only=True)
    lender_type = serializers.CharField(source='lender_type.name', read_only=True)
    

    class Meta:
        model = CustomUser
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 'user_type',
            'company_type', 'role_in_company', 'industry', 'service_type', 
            'tenant_type', 'tenant_subtype', 'lender_type'
        )
