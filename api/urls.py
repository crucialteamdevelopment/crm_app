from django.urls import path
from .views import UserDetail, RegisterView, PasswordResetView, PasswordResetConfirmView, TestView

from users.views import LoginView, CustomTokenRefreshView, LogoutView

urlpatterns = [
    path('', TestView.as_view(), name='status-test'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    ##
    path('register/', RegisterView.as_view(), name='register'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('user/', UserDetail.as_view(), name='user_detail'),
    
]