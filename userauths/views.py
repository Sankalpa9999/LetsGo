from django.shortcuts import redirect, render
from userauths.forms import UserRegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.conf import settings
from userauths.models import User, Profile
from .forms import ProfileUpdateForm
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import PasswordChangeCustomForm
from django.contrib.auth import update_session_auth_hash

# user = settings.AUTH_USER_MODEL

def  register_view(request):
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Account created for {username}')
            new_user = authenticate(username = form.cleaned_data['email'],password=form.cleaned_data['password1'])
            print('User registered')
            login(request,new_user)
            return redirect("index")   

    else:
        print('User not registered')
        form = UserRegisterForm()   
    

    context = {
        'form':form,
    }
    return render(request,'userauths/sign-up.html',context)

def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect('index')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(email = email)
            user = authenticate(request,email = email,password = password)
            
            if user is not None:
                login(request,user)
                messages.success(request,f'Welcome {email}')
                return redirect('index')
            else:
                messages.info(request,'Email or Password is incorrect')
                
        except:
            messages.warning (request,f"User with email {email} does not exist")
            
       
    return render(request,'userauths/sign-in.html')


def logout_view(request):
    logout(request)
    messages.success(request,'You have been logged out')
    return redirect('index')


@login_required
def user_profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        # Create a profile if it doesn't exist
        profile = Profile.objects.create(user=request.user)
    
    return render(request, 'userauths/profile.html', {'profile': profile})



def edit_profile(request):
    profile = Profile.objects.get(user=request.user)
    
    if request.method == 'POST':
        # Handle profile update form
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        # Handle password change form
        password_form = PasswordChangeCustomForm(request.user, request.POST)
        
        if 'save_profile' in request.POST and profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Profile updated successfully.")
        elif 'change_password' in request.POST and password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Important to keep the user logged in after password change
            messages.success(request, "Password changed successfully.")
        else:
            messages.error(request, "Please correct the errors below.")

    else:
        profile_form = ProfileUpdateForm(instance=profile)
        password_form = PasswordChangeCustomForm(request.user)

    return render(request, 'userauths/edit_profile.html', {
        'profile_form': profile_form,
        'password_form': password_form,
    })