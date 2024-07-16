from django.http import HttpResponse
from django.urls import path
from .views import DirectoryListCreateView, DirectoryDetailView, UserFileListCreateView, UserFileDetailView, \
CompanyDetailAPIView, CompanyListCreateAPIView, PhoneNumberListCreateAPIView, PhoneNumberDetailAPIView, ChangePasswordView, LoginView

def test_view(request):
    return HttpResponse("Test view is working")

urlpatterns = [
    path('test/', test_view, name='test_view'),
    path('login/', LoginView.as_view(), name='login'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('directories/', DirectoryListCreateView.as_view(), name='directory-list-create'),
    path('directories/<int:pk>/', DirectoryDetailView.as_view(), name='directory-detail'),
    path('files/', UserFileListCreateView.as_view(), name='userfile-list-create'),
    path('files/<int:pk>/', UserFileDetailView.as_view(), name='userfile-detail'),
    # path('user/<int:pk>/', CustomUserDetailAPIView.as_view(), name='user-detail'),
    path('companies/', CompanyListCreateAPIView.as_view(), name='company-list-create'),
    path('companies/<int:pk>/', CompanyDetailAPIView.as_view(), name='company-detail'),
    path('phone_numbers/', PhoneNumberListCreateAPIView.as_view(), name='phonenumber-list-create'),
    path('phone_numbers/<int:pk>/', PhoneNumberDetailAPIView.as_view(), name='phonenumber-detail'),

]
