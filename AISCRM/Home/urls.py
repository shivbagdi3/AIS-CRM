from django.contrib import admin
from django.urls import path, include
from Home.views import homepage, about, service, contact, s_email, contact_us

urlpatterns = [
    path("", homepage, name='index'),
    path('about/', about, name='about'),
    path('service/', service, name='service'),
    path('contact/', contact, name='contact'),
    path('subscribe/', s_email, name='s_email'),
    path('contact us/', contact_us, name='contactus')    
]