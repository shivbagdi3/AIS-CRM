from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def crm_index(request):
    if request.user.is_authenticated:
        return render(request, 'crm.html')
    else:
        return redirect('login')

def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.. bye..")
    return redirect('crm-index')
