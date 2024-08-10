from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    return render (request,'Home/index.html')

def about(request):
    return render(request,'Home/about.html')

def facilities(request):
    return render(request,'Home/facilities.html')

def contact(request):
    return render(request,'Home/contact.html')