from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.views import TokenRefreshView
from django.conf import settings
from django.contrib.auth import authenticate, logout
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework import generics
from .models import CompanyType, RoleInCompany, Industry, ServiceType, TenantType, TenantSubtype, Company, PhoneNumber, CustomUser
from .serializers import CompanyTypeSerializer, RoleInCompanySerializer, IndustrySerializer, \
    ServiceTypeSerializer, TenantTypeSerializer, TenantSubtypeSerializer, ChangePasswordSerializer, CompanySerializer, PhoneNumberSerializer

from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken


from .serializers import CustomUserSerializer
from rest_framework.decorators import api_view


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def custom_user_detail(request, pk):
    try:
        user = CustomUser.objects.get(pk=pk)
    except CustomUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = CustomUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PATCH':
        serializer = CustomUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # Аутентификация пользователя
        user = authenticate(request=request, email=email, password=password)

        if user is not None:
            # Создание токенов
            refresh_token = RefreshToken.for_user(user)
            access_token = AccessToken.for_user(user)

            # Установка времени истечения для токенов
            refresh_token.set_exp(lifetime=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'])
            access_token.set_exp(lifetime=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'])

            # Получение времени истечения доступа
            access_token_expiration_timestamp = access_token['exp']

            # Установка cookie для refresh token
            response = Response({
                'access_token': str(access_token),
                'access_token_expiration': access_token_expiration_timestamp,
            })

            expires = timezone.now() + settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']
            response.set_cookie(
                key='refresh_token',
                value=str(refresh_token),
                expires=expires,
                httponly=True,
                samesite='None',
                secure=True,
            )

            return response

        else:
            return Response({'error': 'Unable to log in with the provided credentials'}, status=status.HTTP_400_BAD_REQUEST)

    
# class LoginView(APIView):
#     authentication_classes = (TokenAuthentication,)
#     def post(self, request):
#         email = request.data.get('email')
#         password = request.data.get('password')

#         user = authenticate(request=request, email=email, password=password)

#         if user is not None:
#             # Create access token and refresh token
#             refresh_token = RefreshToken.for_user(user)
#             refresh_token.set_exp(lifetime=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'])

#             access_token = AccessToken.for_user(user)
#             access_token.set_exp(lifetime=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'])

#             # Get access token expiration time in timestamp format
#             access_token_expiration_timestamp = access_token['exp']

#             # Cookie name and value
#             cookie_name = 'refresh_token'
#             cookie_value = str(refresh_token)

#             # Set cookie in the response
#             response = Response({
#                 'access_token': str(access_token),
#                 'access_token_expiration': access_token_expiration_timestamp,
#             })
#             expires = timezone.now() + settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']
#             response.set_cookie(cookie_name, cookie_value, expires=expires, httponly=True, samesite='None', secure=True)

#             return response

#         else:
#             return Response({'error': 'Unable to log in with the provided credentials'}, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        # Get refresh token from cookie
        refresh_token = request.COOKIES.get('refresh_token', None)

        if not refresh_token:
            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Add refresh token to request body
        request.data['refresh'] = refresh_token

        # Refresh tokens using refresh token
        response = super().post(request, *args, **kwargs)

        # Get updated tokens from response body
        access_token = response.data.get('access', None)
        refresh_token = response.data.get('refresh', refresh_token)  # Use existing refresh token if not refreshed

        if access_token:
            # Get access token expiration time in timestamp format
            access_token_lifetime = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()
            expires_access_timestamp = timezone.now() + timezone.timedelta(seconds=access_token_lifetime)

            # Return response with updated tokens in body
            return Response({
                'access_token': access_token,
                'access_token_expiration': int(expires_access_timestamp.timestamp()),  # Convert to timestamp
            })

        return response

    def finalize_response(self, request, response, *args, **kwargs):
        # Set SameSite=None and Secure attributes for refresh token cookie
        if 'refresh' in response.data:
            response.set_cookie(
                key='refresh_token',
                value=response.data['refresh'],
                expires=timezone.now() + settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                httponly=True,
                samesite='None',  # Set SameSite=None
                secure=True,  # Set Secure
            )

        return super().finalize_response(request, response, *args, **kwargs)

class LogoutView(APIView):
    def post(self, request):
        # User logout
        logout(request)

        # Clear cookies related to tokens
        response = Response({'success': 'Successfully logged out'})
        response.delete_cookie('refresh_token', samesite='None')  # Delete refresh token cookie

        return response


# CompanyType Views
class CompanyTypeListCreate(generics.ListCreateAPIView):
    queryset = CompanyType.objects.all()
    serializer_class = CompanyTypeSerializer
    permission_classes = (AllowAny,)
    
class CompanyTypeRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = CompanyType.objects.all()
    serializer_class = CompanyTypeSerializer
    permission_classes = [AllowAny]

# RoleInCompany Views
class RoleInCompanyListCreate(generics.ListCreateAPIView):
    queryset = RoleInCompany.objects.all()
    serializer_class = RoleInCompanySerializer
    permission_classes = [AllowAny]

class RoleInCompanyRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = RoleInCompany.objects.all()
    serializer_class = RoleInCompanySerializer
    permission_classes = [AllowAny]

# Industry Views
class IndustryListCreate(generics.ListCreateAPIView):
    queryset = Industry.objects.all()
    serializer_class = IndustrySerializer
    permission_classes = [AllowAny]

class IndustryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Industry.objects.all()
    serializer_class = IndustrySerializer
    permission_classes = [AllowAny]

# ServiceType Views
class ServiceTypeListCreate(generics.ListCreateAPIView):
    queryset = ServiceType.objects.all()
    serializer_class = ServiceTypeSerializer
    permission_classes = [AllowAny]

class ServiceTypeRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceType.objects.all()
    serializer_class = ServiceTypeSerializer
    permission_classes = [AllowAny]

# TenantType Views
class TenantTypeListCreate(generics.ListCreateAPIView):
    queryset = TenantType.objects.all()
    serializer_class = TenantTypeSerializer
    permission_classes = [AllowAny]

class TenantTypeRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = TenantType.objects.all()
    serializer_class = TenantTypeSerializer
    permission_classes = [AllowAny]

# TenantSubtype Views
class TenantSubtypeListCreate(generics.ListCreateAPIView):
    queryset = TenantSubtype.objects.all()
    serializer_class = TenantSubtypeSerializer
    permission_classes = [AllowAny]

class TenantSubtypeRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = TenantSubtype.objects.all()
    serializer_class = TenantSubtypeSerializer
    permission_classes = [AllowAny]
    
    
class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            if not user.check_password(old_password):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()
            return Response({"status": "password set"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CompanyListCreateAPIView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        instance = serializer.save()
        self.return_instance(instance)

    def return_instance(self, instance):
        response_serializer = self.get_serializer(instance)
        self.headers['Location'] = response_serializer.data['id']
        self.response_data = response_serializer.data

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if hasattr(self, 'response_data'):
            response.data = self.response_data
        return response



class CompanyDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [AllowAny]

class PhoneNumberListCreateAPIView(generics.ListCreateAPIView):
    queryset = PhoneNumber.objects.all()
    serializer_class = PhoneNumberSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        instance = serializer.save()
        self.return_instance(instance)
    
    def return_instance(self, instance):
        response_serializer = self.get_serializer(instance)
        self.headers['Location'] = response_serializer.data['id']
        self.response_data = response_serializer.data

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if hasattr(self, 'response_data'):
            response.data = self.response_data
        return response


class PhoneNumberDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PhoneNumber.objects.all()
    serializer_class = PhoneNumberSerializer
    permission_classes = [AllowAny]
    