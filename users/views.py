from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.views import TokenRefreshView
from django.conf import settings
from django.contrib.auth import authenticate, logout

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request=request, email=email, password=password)

        if user is not None:
            # Create access token and refresh token
            refresh_token = RefreshToken.for_user(user)
            refresh_token.set_exp(lifetime=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'])

            access_token = AccessToken.for_user(user)
            access_token.set_exp(lifetime=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'])

            # Get access token expiration time in timestamp format
            access_token_expiration_timestamp = access_token['exp']

            # Cookie name and value
            cookie_name = 'refresh_token'
            cookie_value = str(refresh_token)

            # Set cookie in the response
            response = Response({
                'access_token': str(access_token),
                'access_token_expiration': access_token_expiration_timestamp,
            })
            expires = timezone.now() + settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']
            response.set_cookie(cookie_name, cookie_value, expires=expires, httponly=True, samesite='None', secure=True)

            return response

        else:
            return Response({'error': 'Unable to log in with the provided credentials'}, status=status.HTTP_400_BAD_REQUEST)

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
