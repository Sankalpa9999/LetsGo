from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect


# Create your views here.
def joinpage(request):
    return render(request,'Register/joinpage.html')

