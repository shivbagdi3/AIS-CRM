from django.contrib import admin
from django.urls import path, include
from .views import add_client, view_client, update_client, search_clients, amc_client, update_amc

urlpatterns = [
    path('search-client/', search_clients, name='search-client'),
    path("add-client/", add_client, name='add-client'),
    path("view-client/", view_client, name='view-client'),
    path('update-client/<int:client_id>/', update_client, name='update-client'),
    path('amc-client/', amc_client, name='amc-client'),
    path('amc-update/<int:client_id>/', update_amc, name='amc'),
 ]   
