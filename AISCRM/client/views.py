from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator, Page
from django.db.models import Q
from django.contrib import messages
from client.models import clients
from django.utils import timezone
from datetime import timedelta, datetime
from django.db import IntegrityError

def view_client(request):
    search_query = request.GET.get('search_query', '')
    items_per_page = 15

    if search_query:
        clients_list = clients.objects.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(company_name__icontains=search_query)
        )
    else:
        clients_list = clients.objects.all()

    paginator = Paginator(clients_list, items_per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    max_pages = 5  # Show 5 page numbers
    current_page = page.number
    total_pages = paginator.num_pages

    half_max_pages = max_pages // 2
    start_page = max(1, current_page - half_max_pages)
    end_page = min(total_pages, start_page + max_pages - 1)

    return render(request, 'view_client.html', {
        'page': page,
        'start_page': start_page,
        'end_page': end_page,
    })
def search_clients(request):
    search_query = request.GET.get('search_query', '')
    # Filter clients based on the search query
    clients_list = clients.objects.filter(
        Q(first_name__icontains=search_query) |
        Q(last_name__icontains=search_query) |
        Q(email__icontains=search_query) |
        Q(company_name__icontains=search_query)
    )

    # Serialize the clients
    serialized_clients = [
        {
            'client_id': client.id,
            'first_name': client.first_name,
            'last_name': client.last_name,
            'company_name':client.company_name,
            'email': client.email,
            'phone': client.phone,
            'alternate_no': client.Alternate_no,
            'amc': client.amc_client,
            'gst_no': client.GST_no
        }
        for client in clients_list
    ]

    return JsonResponse({'clients': serialized_clients})

def add_client(request):
    if request.method == "POST":
        f_name = request.POST['first_name']
        l_name = request.POST['last_name']
        C_email = request.POST['email']
        phone = request.POST['phone_num']
        alternet_no = request.POST['alternate_no']
        gst_no = request.POST['GST_NO']
        company_name = request.POST['company_name']
        amc_client = request.POST.get('amc', False)  # Use a default value

        # Convert amc_client to a boolean
        amc_client = amc_client == 'on'
        amc_start = None
        amc_end = None
        try:
            if amc_client:
                amc_start = timezone.now().date()
                amc_end = amc_start + timedelta(365)
            client = clients(
                  first_name= f_name,
                  last_name= l_name,
                  email= C_email,
                  phone= phone,
                  Alternate_no= alternet_no,
                  GST_no= gst_no,
                  company_name= company_name,
                  amc_client= amc_client,
                  amc_start_date = amc_start,
                  amc_end_date = amc_end, 
            )
            client.save()
        except IntegrityError:
            return render(request, 'add_client.html', {'msg': 'Phone number already exists'})
        except Exception as e:
            print(e)

        return redirect('view-client')
    return render(request, 'add_client.html')




def update_client(request, client_id):
    client = get_object_or_404(clients, id=client_id)
    remaining_days = None

    if request.method == 'POST':
        # Update the client's information based on the submitted data
        client.first_name = request.POST['first_name']
        client.last_name = request.POST['last_name']
        client.email = request.POST['email']
        client.phone = request.POST['phone_num']
        client.alternate_no = request.POST.get('alternate_no', None)
        client.GST_no = request.POST['GST_NO']
        client.company_name = request.POST.get('company_name', None)
        client.amc_client = 'amc' in request.POST  # Check if 'amc' is in the POST data

        if client.amc_client:
            amc_start = timezone.now().date()
            amc_end = amc_start + timedelta(365)
            client.amc_start_date = amc_start
            client.amc_end_date = amc_end
        else:
            client.amc_start_date = None  # Reset amc_start_date
            client.amc_end_date = None  # Reset amc_end_date

        client.save()

    if client.amc_start_date and client.amc_end_date:
        current_date = datetime.now().date()
        remaining_days = (client.amc_end_date - current_date).days

    return render(request, 'update_client.html', {'client': client, 'remaining_days': remaining_days})

def amc_clients(request):
    amc_clients = clients.objects.filter(amc_client=True)
    return render(request, 'amc_client.html', {'amc_clients': amc_clients})

