from django.urls import path, include
from .views import add_user


urlpatterns = [
    path('add_user/', add_user, name='add_user')

]