# api/views.py

from rest_framework import generics, status
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .serializers import PasswordResetSerializer, SetNewPasswordSerializer, UserSerializer, RegisterSerializer
from rest_framework.exceptions import NotFound
from users.models import CustomUser
from rest_framework.permissions import IsAuthenticated

from django.conf import settings

from drf_yasg.utils import swagger_auto_schema

User = get_user_model()


class TestView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Returns a simple status message",
        responses={200: "OK"},
        tags=['test']
    )
    def get(self, request):
        return Response({"status": "ok!"})
        
class PasswordResetView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetSerializer

    @swagger_auto_schema(
        operation_description="Reset users password",
        responses={200: "OK"},
        tags=['Auth']
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.get(email=serializer.validated_data['email'])
        except User.DoesNotExist:
            raise NotFound("User with this email does not exist.")

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_url = f"https://crm-project-wight554s-projects.vercel.app/reset-password?uid={uid}&token={token}"

        # Отправка письма с ссылкой на сброс пароля
        send_mail(
            'Password Reset Request',
            f'Hello {user.username},\n\n'
            f'You requested a password reset. Please follow the link below to reset your password:\n'
            f'{reset_url}\n\n'
            f'If you did not request a password reset, please ignore this email.\n\n'
            f'Best regards,\nYour Application Team',
            'mailtrap@demomailtrap.com',  # Укажите адрес отправителя, который используется в настройках Django
            [user.email],  # Укажите адрес получателя
            fail_silently=False,  # Опционально: установите в True, чтобы не поднимать исключение при ошибке отправки
        )

        return Response({"detail": "Password reset e-mail has been sent."}, status=status.HTTP_200_OK)
    
    
class PasswordResetConfirmView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SetNewPasswordSerializer

    @swagger_auto_schema(
        operation_description="Reset users password confirmation",
        responses={200: "OK"},
        tags=['Auth']
    )
        
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            uid = force_str(urlsafe_base64_decode(serializer.validated_data['uid']))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise NotFound("Invalid user or token provided.")

        if default_token_generator.check_token(user, serializer.validated_data['token']):
            user.set_password(serializer.validated_data['new_password'])
            user.save()

            # Отправка уведомления о смене пароля
            send_mail(
                'Password Changed Successfully',
                f'Hello {user.username},\n\n'
                f'Your password has been successfully changed. If you did not initiate this change, please contact support immediately.\n\n'
                f'Best regards,\nYour Application Team',
                'mailtrap@demomailtrap.com',  # Укажите адрес отправителя, который используется в настройках Django
                [user.email],  # Укажите адрес получателя
                fail_silently=False,  # Опционально: установите в True, чтобы не поднимать исключение при ошибке отправки
            )

            return Response({"detail": "Password has been reset with the new password."}, status=status.HTTP_200_OK)
        return Response({"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(generics.CreateAPIView):
    
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    
class UserDetail(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user