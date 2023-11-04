from django.contrib import admin
from django.urls import path, include
from .views import add_client, view_client, update_client, amc_clients

urlpatterns = [
    path("add-client/", add_client, name='add-client'),
    path("view-client/", view_client, name='view-client'),
    path('update-client/<int:client_id>/', update_client, name='update-client'),
    path('amc-clients/', amc_clients, name='amc-clients'),
 ]   
