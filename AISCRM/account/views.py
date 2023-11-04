from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from account.models import Phone
import random
import string
from django.contrib.auth.models import User



def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, "You are logged in... Have a good day")
            return redirect('crm-index')
        else:
            messages.success(request, "Login failed. Please retry again..")
    return render(request, 'login.html')

def generate_verification_code():
    # Generate a random verification code
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def send_verification_email(email, verification_code):
    subject = 'Email Verification'
    message = f'Your verification code is: {verification_code} thank you for joining'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    print(verification_code)

    try:
        send_mail(subject, message, from_email, recipient_list)
    except Exception as e:
        # Handle email sending errors here (if necessary)
        print(f"Failed to send verification email: {str(e)}")
 
def register_user(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_num = request.POST.get('phone_num')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if len(password1) < 8: # verify password len is atlest 8 char
            msg = 'Password must be at least 8 characters long.'
            return render(request, 'register.html', {'msg': msg})

        elif password1 != password2: # verify password match by user
            msg = 'Password not match.'
            return render (request, 'register.html', {'msg': msg})        
        
        elif User.objects.filter(username=email).exists(): # verify that email is unique 
            msg = 'Username already in use. Please choose a different Username.'
            return render(request, 'register.html', {'msg': msg})
        elif len(phone_num) < 10:
            msg = 'Phone number is not valid.'
            return render(request, 'register.html', {'msg': msg})
        
        
        verification_code = generate_verification_code()
        print(verification_code)
        send_verification_email(email, verification_code)

        # Save user details to database (without creating the user yet)
        user_data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone_num': phone_num,
            'password': password1,
            'verification_code': verification_code,
        }
        request.session['user_data'] = user_data  # Store user data temporarily in the session

        return redirect('verify_email')
    
    else:
        return render(request, 'register.html') 


def verify_email(request):
    if request.method == 'POST':
        user_data = request.session.get('user_data')
        if user_data:
            # Compare the entered verification code with the one sent via email
            verification_code = user_data.get('verification_code')
            entered_code = request.POST.get('verification_code')

            if verification_code == entered_code:
                first_name = user_data['first_name']
                last_name = user_data['last_name']
                email = user_data['email']
                password = user_data['password']
                phone_num = user_data['phone_num']

                # Verification successful, create the user
                user = User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    username=email,
                    password=password,
                    )
                
                user_instance = get_object_or_404(User, username=email)
                phone = Phone.objects.create(user = user_instance, phone_number=phone_num)
                phone.save()
               

                del request.session['user_data']  # Clear temporary user data from the session

                return redirect('login')  # Redirect to the login page or a success page
            else:
                msg = 'Invalid verification code. Please try again.'
                return render(request, 'verify_email.html', {'msg': msg})
        else:
            return redirect('register_user')  # If user_data is not found, redirect back to registration
    else:
        return render(request, 'verify_email.html')
    

def request_verification_code(request):
    if request.method == 'POST':
    
        user_data = request.session.get('user_data')
        email = user_data.get('email')

        if email:
            # Generate a new verification code
            verification_code = generate_verification_code()

            try:
                # Send the verification code via email
                send_verification_email(email, verification_code)

                msg = 'Verification code has been sent to your email.'
                return render(request, 'verify_email.html', {'msg': msg})
            except Exception as e:
                # Handle email sending errors, if any
                msg = f'Failed to send verification code: {str(e)}'
                return render(request, 'verify_email.html', {'msg': msg})
        else:
            # Handle the case when 'email' is not present in user_data
            msg = 'Email not found in user_data.'
            return render(request, 'verify_email.html', {'msg': msg})
    return render(request, 'verify_email.html')
