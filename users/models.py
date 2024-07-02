from django.contrib.auth.models import AbstractUser
from django.db import models

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
        ('RESIDENTIAL', 'residential'),
        ('COMMERCIAL', 'commercial'),
     
    )
    TENANT_SUBTYPE = (
        ('COMPANY', 'company'),
        ('EMPLOYEE', 'employee'),
      
    )
    
    user_type = models.CharField(max_length=100, choices=USER_TYPE_CHOICES)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    
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

    def __str__(self):
        return self.username
