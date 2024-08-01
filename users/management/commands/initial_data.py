from django.core.management.base import BaseCommand
from users.models import CompanyType, RoleInCompany, Industry, ServiceType, TenantType, TenantSubtype

class Command(BaseCommand):
    help = 'Load initial data into the database'

    def handle(self, *args, **kwargs):
        # Add initial data for CompanyType
        company_types = [
            'Investment Fund', 'Family Office', 'Individual', 'Residential', 'Commercial', 'Other'
        ]
        for name in company_types:
            CompanyType.objects.get_or_create(name=name)

        # Add initial data for RoleInCompany
        roles_in_company = [
            'Principal', 'Director', 'Representative', 'Broker', 'CEO', 'Co-Founder', 'Executive', 'Founder', 'Other'
        ]
        for name in roles_in_company:
            RoleInCompany.objects.get_or_create(name=name)

        # Add initial data for Industry
        industries = [
            'Retail', 'Law', 'Architecture', 'Fashion', 'Entertainment', 'Hospitality', 'Restaurant', 'Jewelry', 'Other'
        ]
        for name in industries:
            Industry.objects.get_or_create(name=name)

        # Add initial data for ServiceType
        service_types = [
            'Accountant', 'Appraiser', 'Architect', 'Boiler', 'Carpentry', 'CCTV (Security Cameras)', 'Doors',
            'Earthwork', 'Electrical', 'Elevator', 'Event Planner', 'Flooring', 'Foundation', 'Framing', 
            'General Contractor', 'General Repairs', 'HVAC', 'Inspector', 'Interior Designer', 'IT', 'Landscaping',
            'Lawyer', 'Marketing', 'Mechanical', 'Metal Work', 'Moving', 'Paint', 'Plumbing', 'Roofing', 
            'Scaffolding', 'Sitework Protection', 'Violation Resolution', 'Windows', 'Other'
        ]
        for name in service_types:
            ServiceType.objects.get_or_create(name=name)

        # Add initial data for TenantType
        tenant_types = ['Residential', 'Commercial']
        for name in tenant_types:
            TenantType.objects.get_or_create(name=name)

        # Add initial data for TenantSubtype
        tenant_subtypes = ['Company', 'Employee']
        for name in tenant_subtypes:
            TenantSubtype.objects.get_or_create(name=name)

        self.stdout.write(self.style.SUCCESS('Successfully loaded initial data'))
