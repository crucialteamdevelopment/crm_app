from django.core.management.base import BaseCommand
from properties.models import PropertyType

class Command(BaseCommand):
    help = 'Load initial property types into the database'

    def handle(self, *args, **kwargs):
        # Add initial data for PropertyType
        property_types = [
            ('Office', 'Office'),
            ('Industrial', 'Industrial'),
            ('Retail', 'Retail'),
            ('Shopping Center', 'Shopping Center'),
            ('Multifamily', 'Multifamily'),
            ('Specialty', 'Specialty'),
            ('Healthcare', 'Healthcare'),
            ('Hospitality', 'Hospitality'),
            ('Sports and Entertainment', 'Sports and Entertainment'),
            ('Land', 'Land'),
            ('Residential', 'Residential'),
            ('Restaurant', 'Restaurant'),
        ]
        for name, description in property_types:
            PropertyType.objects.get_or_create(name=name, description=description)

        self.stdout.write(self.style.SUCCESS('Successfully loaded initial property types'))
