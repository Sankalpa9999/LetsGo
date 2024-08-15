from django.shortcuts import render,redirect
from django.contrib.auth import logout

# Create your views here.


def login(request):
    return render(request, 'users/login.html')

def sanjog(request):
    return render(request,'users/sanjog.html')


def logout_view(request):
    logout(request)
    return redirect('/')