from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from client.models import clients

def view_client(request):
    client = clients.objects.all()
    return render(request, 'view_client.html', {'client':client})

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
        try:
            client = clients(
                  first_name= f_name,
                  last_name= l_name,
                  email= C_email,
                  phone= phone,
                  Alternate_no= alternet_no,
                  GST_no= gst_no,
                  company_name= company_name,
                  amc_client= amc_client
            )
            client.save()
        except Exception as e:
            print(e)

        return render(request, 'add_client.html')
    return render(request, 'add_client.html')


def update_client(request, client_id):
    client = get_object_or_404(clients, id=client_id)

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
        
        # Save the changes to the client object
        client.save()

        return redirect('view-client')  # Redirect to the view-client page after updating

    return render(request, 'update_client.html', {'client': client})

def amc_clients(request):
    amc_clients = clients.objects.filter(amc_client=True)
    return render(request, 'amc_client.html', {'amc_clients': amc_clients})

