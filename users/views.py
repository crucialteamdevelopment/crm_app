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
            # Создаем токен доступа и токен обновления
            refresh_token = RefreshToken.for_user(user)
            refresh_token.set_exp(lifetime=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'])

            access_token = AccessToken.for_user(user)
            access_token.set_exp(lifetime=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'])

            # Получаем время истечения access token в формате таймстампа
            access_token_expiration_timestamp = access_token['exp']

            # Имя и значение куки
            cookie_name = 'refresh_token'
            cookie_value = str(refresh_token)

            # Устанавливаем куку в ответе
            response = Response({
                'access_token': str(access_token),
                'access_token_expiration': access_token_expiration_timestamp,
            })
            expires = timezone.now() + settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']
            response.set_cookie(cookie_name, cookie_value, expires=expires, httponly=True, samesite='None', secure=True)

            return response

        else:
            return Response({'error': 'Невозможно войти с предоставленными учетными данными'}, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenRefreshView(TokenRefreshView):

    def post(self, request, *args, **kwargs):
        # Получаем refresh token из куки
        refresh_token = request.COOKIES.get('refresh_token', None)

        if not refresh_token:
            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Добавляем refresh token в тело запроса
        request.data['refresh'] = refresh_token

        # Обновляем токены с использованием refresh token
        response = super().post(request, *args, **kwargs)

        # Получаем обновленные токены из тела ответа
        access_token = response.data.get('access', None)
        refresh_token = response.data.get('refresh', refresh_token)  # Используем существующий refresh token, если он не обновлялся

        if access_token:
            # Получаем время истечения access token в формате таймстампа
            access_token_lifetime = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()
            expires_access_timestamp = timezone.now() + timezone.timedelta(seconds=access_token_lifetime)

            # Возвращаем response с обновленными токенами в теле
            return Response({
                'access_token': access_token,
                'access_token_expiration': int(expires_access_timestamp.timestamp()),  # Преобразуем в timestamp
            })

        return response

    def finalize_response(self, request, response, *args, **kwargs):
        # Устанавливаем атрибуты SameSite=None и Secure для куки с refresh token
        if 'refresh' in response.data:
            response.set_cookie(
                key='refresh_token',
                value=response.data['refresh'],
                expires=timezone.now() + settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                httponly=True,
                samesite='None',  # Устанавливаем SameSite=None
                secure=True,  # Устанавливаем Secure
            )

        return super().finalize_response(request, response, *args, **kwargs)

class LogoutView(APIView):

    def post(self, request):
        # Выход пользователя
        logout(request)

        # Очистка кук, связанных с токенами
        response = Response({'success': 'Successfully logged out'})
        response.delete_cookie('refresh_token', samesite='None')  # Удаляем куку с refresh token

        return response

