from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    class Meta:
        db_table = 'users'
    
    USER_TYPE_CHOICES = (
        ('broker_real_estate', 'Broker (Real Estate)'),
        ('broker_mortgage', 'Broker (Mortgage)'),
        ('owner', 'Owner'),
        ('lender', 'Lender'),
        ('service_provider', 'Service Provider'),
        ('tenant', 'Tenant'),
        ('salesperson_real_estate', 'Salesperson (Real Estate)'),
        ('salesperson_mortgage', 'Salesperson (Mortgage)'),
    )
    
    COMPANY_TYPE_CHOICES = (
        ('investment_fund', 'Investment Fund'),
        ('family_office', 'Family Office'),
        ('individual', 'Individual'),
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('other', 'Other'),
    )
    
    ROLE_IN_COMPANY_CHOICES = (
        ('principal', 'Principal'),
        ('director', 'Director'),
        ('representative', 'Representative'),
        ('broker', 'Broker'),
        ('ceo', 'CEO'),
        ('co-founder', 'Co-Founder'),
        ('executive', 'Executive'),
        ('founder', 'Founder'),
        ('other', 'Other'),
    )
    
    SERVICE_TYPE = (
        ('accountant', 'Accountant'),
        ('appraiser', 'Appraiser'),
        ('architect', 'Architect'),
        ('boiler', 'Boiler'),
        ('carpentry', 'Carpentry'),
        ('cctv', 'CCTV (Security Cameras)'),
        ('doors', 'Doors'),
        ('earthwork', 'Earthwork'),
        ('electrical', 'Electrical'),
        ('elevator', 'Elevator'),
        ('event_planner', 'Event Planner'),
        ('flooring', 'Flooring'),
        ('foundation', 'Foundation'),
        ('framing', 'Framing'),
        ('general_contractor', 'General Contractor'),
        ('general_repairs', 'General Repairs'),
        ('hvac', 'HVAC'),
        ('inspector', 'Inspector'),
        ('interior_designer', 'Interior Designer'),
        ('it', 'IT'),
        ('landscaping', 'Landscaping'),
        ('lawyer', 'Lawyer'),
        ('marketing', 'Marketing'),
        ('mechanical', 'Mechanical'),
        ('metal_work', 'Metal Work'),
        ('moving', 'Moving'),
        ('paint', 'Paint'),
        ('plumbing', 'Plumbing'),
        ('roofing', 'Roofing'),
        ('scaffolding', 'Scaffolding'),
        ('sitework_protection', 'Sitework Protection'),
        ('violation_resolution', 'Violation Resolution'),
        ('windows', 'Windows'),
        ('other', 'Other')
    )
    
    INDUSTRY_CHOICES = (
        ('retail', 'Retail'),
        ('law', 'Law'),
        ('architecture', 'Architecture'),
        ('fashion', 'Fashion'),
        ('entertainment', 'Entertainment'),
        ('hospitality', 'Hospitality'),
        ('restaurant', 'Restaurant'),
        ('jewelry', 'Jewelry'),
        ('other', 'Other'),
    )
    
    TENANT_TYPE = (
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
     
    )
    TENANT_SUBTYPE = (
        ('company', 'Company'),
        ('employee', 'Employee'),
      
    )
    
    user_type = models.CharField(max_length=100, choices=USER_TYPE_CHOICES)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    
    companies = models.ManyToManyField('Company', related_name='users', blank=True)
    phone_numbers = models.ManyToManyField('PhoneNumber', related_name='users', blank=True)
   
   
    company_type = models.CharField(max_length=100, choices=COMPANY_TYPE_CHOICES, blank=True, null=True)
    role_in_company = models.CharField(max_length=100, choices=ROLE_IN_COMPANY_CHOICES, blank=True, null=True)
    industry = models.CharField(max_length=100, choices=INDUSTRY_CHOICES, blank=True, null=True)
    service_type = models.CharField(max_length=100, choices=SERVICE_TYPE, blank=True, null=True)
    lender_type = models.CharField(max_length=255, null=True, blank=True)
    headquarters = models.CharField(max_length=255, null=True, blank=True)
    established = models.CharField(max_length=255, null=True, blank=True)
    
    mailing_address = models.CharField(max_length=100, blank=True, null=True)
    tenant_type = models.CharField(max_length=100, choices=TENANT_TYPE, blank=True, null=True)
    tenant_subtype = models.CharField(max_length=100, choices=TENANT_SUBTYPE, blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']



class Company(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100, choices=CustomUser.COMPANY_TYPE_CHOICES)
    about = models.TextField(blank=True, null=True)
     
    def __str__(self):
        return self.name

class PhoneNumber(models.Model):
    number = models.CharField(max_length=15)

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



