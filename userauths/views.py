from django.shortcuts import redirect, render
from userauths.forms import UserRegisterForm,VendorRegistrationForm,UserUpdateForm,ProfileUpdateForm, PasswordChangeCustomForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.conf import settings
from userauths.models import User, Profile, ContactUs

from .models import Profile
from django.contrib.auth.decorators import login_required

from django.contrib.auth import update_session_auth_hash

from django.contrib.auth import update_session_auth_hash
from Home.models import Vendor

from django.contrib import messages

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



@login_required
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        password_form = PasswordChangeCustomForm(request.user, request.POST)

        if 'save_profile' in request.POST:
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, "Profile updated successfully.")
            else:
                messages.error(request, "Please correct the errors in the form.")

        elif 'change_password' in request.POST and password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password changed successfully.")

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)
        password_form = PasswordChangeCustomForm(request.user)

    return render(request, 'userauths/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'password_form': password_form,
    })
    
    
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeCustomForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('userauths:edit_profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeCustomForm(request.user)
    return render(request, 'userauths/change_password.html', {'form': form})




def contactUs(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        phone = request.POST.get('phone')
        
        ContactUs.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message,
            phone=phone
        )
        
        messages.success(request, "Thank you for contacting us. We will get back to you soon.")
        return redirect('userauths:contact')  # Changed from render to redirect
    
    # Pre-fill form for logged-in users
    initial_data = {}
    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user).first()
        initial_data = {
            'name': request.user.username,
            'email': request.user.email,
            'phone': profile.phone if profile else ''
        }
    
    return render(request, 'userauths/contact.html', {'initial_data': initial_data})


@login_required
def register_as_vendor(request):
    if Vendor.objects.filter(user=request.user).exists():
        return redirect('/useradmin/dashboard/')

    if request.method == 'POST':
        form = VendorRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            vendor = form.save(commit=False)
            vendor.user = request.user
            vendor.save()
            messages.success(request, "Vendor registration successful!")

            return redirect('/useradmin/dashboard/')  # redirect after success
    else:
        form = VendorRegistrationForm()
    
    return render(request, 'userauths/vendor_register.html', {'form': form})


