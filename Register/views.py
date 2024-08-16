
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import RegistrationForm, LoginForm
from django.contrib.auth.backends import ModelBackend
from allauth.socialaccount.models import SocialAccount




# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Create the user
            user = User.objects.create_user(
                username=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            # Redirect to the login page after successful registration
            return redirect('login')
    else:
        form = RegistrationForm()

    return render(request, 'Register/register.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Retrieve the user based on the email
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                form.add_error(None, "Invalid email or password")
                return render(request, 'Register/login.html', {'form': form})
            
            # Authenticate the user using the username (name) and password
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                return redirect('choose')  # Redirect to the 'choose' page after successful login
            else:
                form.add_error(None, "Invalid email or password")
    else:
        form = LoginForm()

    return render(request, 'Register/login.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('register')

def choose(request):
    return render(request,'Register/choose.html')