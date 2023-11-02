from django.shortcuts import render, redirect

def add_user(request):
    return render(request, 'add_user.html')