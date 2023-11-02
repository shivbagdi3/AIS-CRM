from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def crm_index(request):
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
    return render(request, 'crm.html')

def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.. bye..")
    return redirect('crm-index')
