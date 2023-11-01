from django.shortcuts import render
from Home.models import EmailAddress, contactus

def homepage(request):
    return render(request, "index.html")

def about(request):
    return render(request, 'about.html')

def service(request):
    return render(request, 'service.html')

def contact(request):
    return render(request, 'contact.html')

def s_email(request):
    if request.method == "POST":
         email = request.POST.get('email')
          # Check if the email address already exists in the database
         if not EmailAddress.objects.filter(email=email).exists():
            EmailAddress.objects.create(email=email)

         return render(request, 'index.html')
    return render(request, 'index.html')


def contact_us(request):
    if request.method == "POST":
        name = request.POST.get('name')
        mail = request.POST.get('mail')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if not name or not mail or not subject or not message:
            return render(request, 'contact.html', {'msg': 'All fields are required.'})

        try:
            # Create a new entry in the contactus table
            contactus.objects.create(
                name=name,
                email=mail,
                subject=subject,
                message=message,
            )
            return render(request, 'contact.html', {'msg': 'Form submitted successfully.'})
        except Exception as e:
            return render(request, 'contact.html',{'msg': f'An error occurred: {str(e)}'})

    return render(request, 'contact.html')