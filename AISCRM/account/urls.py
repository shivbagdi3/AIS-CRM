from django.urls import path, include
from account.views import register_user, verify_email, request_verification_code, user_login


urlpatterns = [
    path('login/', user_login, name='login'),
    path('register/', register_user, name='register'),
    path('verify/', verify_email, name='verify_email'),
    path('request_verification_code/', request_verification_code, name='resend_code')
]