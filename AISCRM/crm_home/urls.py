from django.urls import path, include
from crm_home.views import crm_index

urlpatterns = [
    path('crm-index/', crm_index, name='crm-index'),
]
