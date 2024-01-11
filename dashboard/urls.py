from django.urls import path
from dashboard.views import dashboard, ExportCSVView, login_user, logout_user

urlpatterns = [
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('', dashboard, name='dashboard'),
    path('export-csv/<str:app_name>/<str:model_name>/', ExportCSVView.as_view(), name='export_csv'),   
]