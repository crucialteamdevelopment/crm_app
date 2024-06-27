from django.db import models
from users.models import CustomUser
from django.conf import settings


# Create your models here.


class Property(models.Model):
    class Meta:
        db_table = 'properties'

    PROPERTY_TYPE_CHOICES = [
        ('office', 'Office'),
        ('industrial', 'Industrial'),
        ('retail', 'Retail'),
        ('shopping_center', 'Shopping Center'),
        ('multifamily', 'Multifamily'),
        ('specialty', 'Specialty'),
        ('healthcare', 'Healthcare'),
        ('hospitality', 'Hospitality'),
        ('sports_entertainment', 'Sports and Entertainment'),
        ('land', 'Land'),
        ('residential', 'Residential'),
        ('restaurant', 'Restaurant'),
    ]

    street_address = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=20)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    neighborhood = models.CharField(max_length=150, null=True, blank=True)
    building_name = models.CharField(max_length=150, null=True, blank=True)
    number_of_floors = models.PositiveIntegerField()
    holding_company = models.CharField(max_length=100)
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPE_CHOICES)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='properties')

    def __str__(self):
        return f'{self.property_type} at {self.street_address}'

class PropertyType(models.Model):
    class Meta:
        db_table = 'properties_types'

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class PropertyUnit(models.Model):
    class Meta:
        db_table = 'properties_units'

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    type = models.ForeignKey(PropertyType, on_delete=models.SET_NULL, null=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='units')
    location = models.CharField(max_length=255)
    size = models.DecimalField(max_digits=10, decimal_places=2)  # For example, square meters
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class PropertyImage(models.Model):
    class Meta:
        db_table = 'property_images'

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property_images/')
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'Image for {self.property.street_address}'


class Violation(models.Model):
    class Meta:
        db_table = 'violation'
        
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    description = models.TextField()
    date_reported = models.DateField()
    date_resolved = models.DateField(blank=True, null=True)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    property_unit = models.ForeignKey(PropertyUnit, on_delete=models.CASCADE)
    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='reported_violations')
    resolved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='resolved_violations')

    def __str__(self):
        return f"Violation {self.id} at {self.property_unit.name}"

    class Meta:
        ordering = ['-date_reported']

class Bookmark(models.Model):
    class Meta:
        db_table = 'bookmarks'
        
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookmarks')
    property_unit = models.ForeignKey(PropertyUnit, on_delete=models.CASCADE, related_name='bookmarks')
    created_at = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s bookmark for {self.property_unit.name}"

    class Meta:
        unique_together = ('user', 'property_unit')
        ordering = ['-created_at']