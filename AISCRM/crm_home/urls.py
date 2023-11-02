from django.urls import path, include
from crm_home.views import crm_index, user_logout

urlpatterns = [
    path('crm/', crm_index, name='crm-index'),
    path('logout/', user_logout, name='logout'),
]
