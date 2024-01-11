from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator, Page, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.contrib import messages
from client.models import clients, Feedback, update_at
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import timedelta, datetime
from django.db import IntegrityError

def view_client(request):
    items_per_page = 15   
    clients_list = clients.objects.all().order_by('id')  # Replace 'id' with the field you want to order by     
    page_number = request.GET.get('page', 1)  # Default to page 1 if not provided or invalid   
    paginator = Paginator(clients_list, items_per_page)
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page.
        page = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver the last page.
        page = paginator.page(paginator.num_pages)

    max_pages = 5
    current_page = page.number
    total_pages = paginator.num_pages

    half_max_pages = max_pages // 2
    start_page = max(1, current_page - half_max_pages)
    end_page = min(total_pages, start_page + max_pages - 1)

    return render(request, 'view_clients.html', {
        'page': page,
        'start_page': start_page,
        'end_page': end_page,
    })
    
def amc_client(request):
    clients_list = clients.objects.filter(amc_client=True)
    items_per_page = 15

    for client in clients_list:
    # Calculate remaining days for each client
        if client.amc_end_date and client.amc_end_date >= datetime.now().date():
            remaining_days = (client.amc_end_date - datetime.now().date()).days
            client.remaining_days = remaining_days
        else:
            client.remaining_days = "N/A"
    paginator = Paginator(clients_list, items_per_page)
    page_number = request.GET.get('page', 1)  # Default to page 1 if not provided or invalid

    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page.
        page = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver the last page.
        page = paginator.page(paginator.num_pages)

    max_pages = 5
    current_page = page.number
    total_pages = paginator.num_pages

    half_max_pages = max_pages // 2
    start_page = max(1, current_page - half_max_pages)
    end_page = min(total_pages, start_page + max_pages - 1)

    return render(request, 'amc_client.html', {
        'page': page,
        'remaining_days_list': [client.remaining_days for client in page.object_list],
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
        Q(company_name__icontains=search_query) |
        Q(phone__icontains=search_query)
    )
    for client in clients_list:
        # Calculate remaining days for each client
        if client.amc_end_date and client.amc_end_date >= datetime.now().date():
            remaining_days = (client.amc_end_date - datetime.now().date()).days
            client.remaining_days = remaining_days
        else:
            client.remaining_days = "N/A"
    # Serialize the clients
    serialized_clients = [
        {
            'client_id': client.id,
            'first_name': client.first_name,
            'last_name': client.last_name,
            'company_name':client.company_name,
            'email': client.email,
            'phone': str(client.phone),
            'alternate_no': str(client.Alternate_no),
            'amc': client.amc_client,
            'gst_no': client.GST_no,
            'remaining_days': client.remaining_days
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
        feedback = request.POST['feedback']
        

        if clients.objects.filter(email = C_email).exists():
            return render(request, 'add_client.html', {'msg': 'This Email already exists'})
        
        elif len(phone) < 10:
            return render(request, 'add_client.html', {'msg': 'enter Atlest 10 Number'})
        
        elif clients.objects.filter(phone = phone).exists():
            return render(request, 'add_client.html', {'msg': 'This Phone Number Already exists'})
        else:             
        # Convert amc_client to a boolean
            amc_client = amc_client == 'on'
            amc_start = None
            amc_end = None
            try:
                if amc_client:
                    amc_start = timezone.now().date()
                    amc_end = amc_start + timedelta(365)
                client = clients(
                    created_at = timezone.now().date(),
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

                feedback_obj = Feedback(feedback=feedback, feedback_id=client)
                feedback_obj.save()
                
            except IntegrityError:
                return render(request, 'add_client.html', {'msg': 'Phone number already exists'})
            except Exception as e:
                print(e)

            return redirect('view-client')
    return render(request, 'add_client.html')




def update_client(request, client_id):
    client = get_object_or_404(clients, id=client_id)
    feedBack = Feedback.objects.filter(feedback_id=client).order_by('-feed_back')
    remaining_days = None
    updates = update_at.objects.filter(update_id=client).order_by('-update')

    if request.method == 'POST':
        # Update the client's information based on the submitted data
        client.first_name = request.POST['first_name']
        client.last_name = request.POST['last_name']
        client.email = request.POST['email']
        client.phone = request.POST['phone_num']
        client.Alternate_no = request.POST.get('alternate_no', None)
        client.GST_no = request.POST['GST_NO']
        client.company_name = request.POST.get('company_name', None)
        feedback = request.POST['feedback']      

        client.save()

        feedback_obj = Feedback(feed_back=feedback, feedback_id=client, update_by=request.user)
        feedback_obj.save()

        update = update_at(update=timezone.now().date(), update_id=client, update_by=request.user)
        update.save()

    if client.amc_start_date and client.amc_end_date:
        current_date = datetime.now().date()
        remaining_days = (client.amc_end_date - current_date).days

    return render(request, 'update.html', {'client': client, 'remaining_days': remaining_days, 'updates':updates, 'feedback':feedBack})

def update_amc(request, client_id):
    client = get_object_or_404(clients, id=client_id)
    amc_start = timezone.now().date()
    amc_end = amc_start + timedelta(365)
    client.amc_start_date = amc_start
    client.amc_end_date = amc_end

    client.save()
    return redirect('view-client')




