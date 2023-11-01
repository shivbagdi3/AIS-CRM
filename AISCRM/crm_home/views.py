from django.shortcuts import render

def crm_index(request):
    return render(request, 'crm.html')

