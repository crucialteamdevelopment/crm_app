from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class CustomUser(AbstractUser):
    class Meta:
        db_table = 'users'
    
    USER_TYPE_CHOICES = (
        ('broker_real_estate', 'Broker (Real Estate)'),
        ('broker_mortgage', 'Broker (Mortgage)'),
        ('salesperson_real_estate', 'Salesperson Real Estate'),
        ('salesperson_mortgage', 'Mortgage salesperson'),
        ('owner', 'Owner'),
        ('lender', 'Lender'),
        ('service_provider', 'Service Provider'),
        ('tenant', 'Tenant'),
    )
    
    user_type = models.CharField(max_length=100, choices=USER_TYPE_CHOICES)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    
    company_type = models.ForeignKey('CompanyType', on_delete=models.SET_NULL, null=True, blank=True)
    role_in_company = models.ForeignKey('RoleInCompany', on_delete=models.SET_NULL, null=True, blank=True)
    industry = models.ForeignKey('Industry', on_delete=models.SET_NULL, null=True, blank=True)
    service_type = models.ForeignKey('ServiceType', on_delete=models.SET_NULL, null=True, blank=True)
    lender_type = models.CharField(max_length=255, null=True, blank=True)
    headquarters = models.CharField(max_length=255, null=True, blank=True)
    established = models.CharField(max_length=255, null=True, blank=True)
    
    mailing_address = models.CharField(max_length=100, blank=True, null=True)
    tenant_type = models.ForeignKey('TenantType', on_delete=models.SET_NULL, null=True, blank=True)
    tenant_subtype = models.ForeignKey('TenantSubtype', on_delete=models.SET_NULL, null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username



# class LenderType(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.CharField(max_length=100, blank=True, null=True)

#     def __str__(self):
#         return self.name
    
    
class CompanyType(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class RoleInCompany(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class Industry(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class ServiceType(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class TenantType(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class TenantSubtype(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(max_length=100)
    about = models.TextField(blank=True, null=True)
    company_type = models.ForeignKey(CompanyType, on_delete=models.CASCADE, related_name='companies', null=True)
    user = models.ManyToManyField('CustomUser', related_name='companies', blank=True)
    
    
    def __str__(self):
        return self.name



class PhoneNumber(models.Model):
    number = models.CharField(max_length=15)
    title = models.CharField(max_length=15, null=True, blank=True)
    user = models.ManyToManyField('CustomUser', related_name='phone_numbers', blank=True)
    
    def __str__(self):
        return self.number
    
    
class Directory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='directories')
    name = models.CharField(max_length=255)
    parent_directory = models.ForeignKey('self', on_delete=models.CASCADE, related_name='subdirectories', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class UserFile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='files')
    directory = models.ForeignKey(Directory, on_delete=models.CASCADE, related_name='files', null=True, blank=True)
    file = models.FileField(upload_to='user_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_type = models.CharField(max_length=50, blank=True, null=True)
    tag = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.file.name}"
