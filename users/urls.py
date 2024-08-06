from django.urls import path
from .views import (CompanyTypeListCreate, CompanyTypeRetrieveUpdateDestroy, LenderTypeListCreateAPIView, LenderTypeRetrieveUpdateDestroyAPIView,
                    RoleInCompanyListCreate, RoleInCompanyRetrieveUpdateDestroy,
                    IndustryListCreate, IndustryRetrieveUpdateDestroy,
                    ServiceTypeListCreate, ServiceTypeRetrieveUpdateDestroy,
                    TenantTypeListCreate, TenantTypeRetrieveUpdateDestroy,
                    TenantSubtypeListCreate, TenantSubtypeRetrieveUpdateDestroy, ChangePasswordView, CompanyListCreateAPIView, \
                    CompanyDetailAPIView, PhoneNumberDetailAPIView, PhoneNumberListCreateAPIView, custom_user_detail)

urlpatterns = [
    path('user/<int:pk>/', custom_user_detail, name='custom_user_detail'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('companies/', CompanyListCreateAPIView.as_view(), name='company-list-create'),
    path('companies/<int:pk>/', CompanyDetailAPIView.as_view(), name='company-detail'),
    path('phone_numbers/', PhoneNumberListCreateAPIView.as_view(), name='phonenumber-list-create'),
    path('phone_numbers/<int:pk>/', PhoneNumberDetailAPIView.as_view(), name='phonenumber-detail'),

    path('company-types/', CompanyTypeListCreate.as_view(), name='companytype-list-create'),
    path('company-types/<int:pk>/', CompanyTypeRetrieveUpdateDestroy.as_view(), name='companytype-detail'),
    
    path('roles-in-company/', RoleInCompanyListCreate.as_view(), name='roleincompany-list-create'),
    path('roles-in-company/<int:pk>/', RoleInCompanyRetrieveUpdateDestroy.as_view(), name='roleincompany-detail'),
    
    path('industries/', IndustryListCreate.as_view(), name='industry-list-create'),
    path('industries/<int:pk>/', IndustryRetrieveUpdateDestroy.as_view(), name='industry-detail'),
    
    path('service-types/', ServiceTypeListCreate.as_view(), name='servicetype-list-create'),
    path('service-types/<int:pk>/', ServiceTypeRetrieveUpdateDestroy.as_view(), name='servicetype-detail'),
    
    path('tenant-types/', TenantTypeListCreate.as_view(), name='tenanttype-list-create'),
    path('tenant-types/<int:pk>/', TenantTypeRetrieveUpdateDestroy.as_view(), name='tenanttype-detail'),
    
    path('tenant-subtypes/', TenantSubtypeListCreate.as_view(), name='tenantsubtype-list-create'),
    path('tenant-subtypes/<int:pk>/', TenantSubtypeRetrieveUpdateDestroy.as_view(), name='tenantsubtype-detail'),
    path('lender-types/', LenderTypeListCreateAPIView.as_view(), name='lender-type-list-create'),
    path('lender-types/<int:pk>/', LenderTypeRetrieveUpdateDestroyAPIView.as_view(), name='lender-type-detail'),

]
