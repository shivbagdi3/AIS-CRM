from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from client.models import clients
from django.contrib import messages
import csv
from django.http import HttpResponse
from django.views.generic import View
from django.apps import apps

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, "You are logged in... Have a good day")
            return redirect('dashboard')
        else:
            messages.success(request, "Login failed. Please retry again..")
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('login')
    

@login_required
def dashboard(request):
    amc_clients = clients.objects.filter(amc_client=True).count()
    non_amc = clients.objects.filter(amc_client=False).count()
    total_client = clients.objects.all().count()

    labels = ["AMC Clients", "Non-AMC Clients", "Total Clients"]
    series = [amc_clients, non_amc, total_client]
    difference_series = [amc_clients, non_amc, total_client - amc_clients - non_amc]

    return render(request, 'dashboard.html', 
                  {'labels': labels, 
                   'series': series, 
                   'difference_series': difference_series,
                   'total_clients': total_client,                
                   })

class ExportCSVView(View):
    def get(self, request, app_name, model_name, *args, **kwargs):
        app_model = apps.get_model(app_name, model_name)
        if not app_model:
            return HttpResponse("Model not found.", status=404)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={model_name}_export.csv'

        writer = csv.writer(response)

        # Write header row
        header_row = [field.verbose_name for field in app_model._meta.fields]  # Get field names dynamically
        writer.writerow(header_row)

        # Apply filters if provided in the URL parameters
        filters = {}
        for key, value in request.GET.items():
            filters[key] = value

        # Check if any filters are provided
        if filters:
            queryset = app_model.objects.filter(**filters)
        else:
            queryset = app_model.objects.all()

        # Write data rows
        for obj in queryset:
            data_row = [getattr(obj, field.name) for field in app_model._meta.fields]
            writer.writerow(data_row)

        return response