# your_app/authentication.py
from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomJWTAuthentication(JWTAuthentication):
    pass  # Этот класс остается пустым для простоты примера
