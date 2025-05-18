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




from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm


from django.contrib.auth.tokens import default_token_generator

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse
from django.core.mail import send_mail

from django.contrib.auth.tokens import default_token_generator







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
        profile = Profile.objects.create(user=request.user)
    
    return render(request, 'userauths/profile.html', {
        'profile': profile,
        'license_image': profile.user.license_image,
        'citizenship_image': profile.user.citizenship_image
    })


@login_required
def edit_profile(request):
    """
    Handle the user's profile editing, including updating personal details,
    profile image, and password change functionality.
    """
    # Retrieve the user's profile instance
    profile = Profile.objects.get(user=request.user)
    
    if request.method == 'POST':
        # Initialize forms with POST data and files
        user_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        password_form = PasswordChangeCustomForm(request.user, request.POST)

        # Handle saving the profile updates
        if 'save_profile' in request.POST:
            if user_form.is_valid() and profile_form.is_valid():
                # Save user form and update user instance
                user = user_form.save(commit=False)

                # Handle file uploads for images if provided
                if 'profile_image' in request.FILES:
                    user.profile_image = request.FILES['profile_image']
                if 'license_image' in request.FILES:
                    user.license_image = request.FILES['license_image']
                if 'citizenship_image' in request.FILES:
                    user.citizenship_image = request.FILES['citizenship_image']
                
                # Save the updated user instance
                user.save()
                # Save the associated profile form
                profile_form.save()

                # Display success message
                messages.success(request, "Your profile has been updated successfully.")
            else:
                # Display error message if form validation fails
                messages.error(request, "Please correct the errors in the form before submitting.")

        # Handle password change request
        elif 'change_password' in request.POST and password_form.is_valid():
            # Save the new password and update session
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password has been changed successfully.")

    else:
        # Initialize forms with existing user and profile data
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)
        password_form = PasswordChangeCustomForm(request.user)

    # Render the profile edit template with forms and necessary context
    return render(request, 'userauths/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'password_form': password_form,
        'license_image': request.user.license_image,
        'citizenship_image': request.user.citizenship_image,
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
    # If already a vendor, redirect to dashboard
    if Vendor.objects.filter(user=request.user).exists():
        messages.info(request, "You are already registered as a vendor.")
        return redirect('useradmin:dashboard')

    if request.method == 'POST':
        form = VendorRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            vendor = form.save(commit=False)
            vendor.user = request.user
            vendor.save()
            messages.success(request, "Vendor registration successful! You can now access the vendor dashboard.")
            return redirect('useradmin:dashboard')
    else:
        form = VendorRegistrationForm()
    
    return render(request, 'userauths/vendor_register.html', {'form': form})



# Password Reset Request View
def password_reset_view(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            associated_users = User.objects.filter(email=email)
            if associated_users.exists():
                for user in associated_users:
                    token = default_token_generator.make_token(user)
                    uid = urlsafe_base64_encode(str(user.pk).encode('utf-8'))
                    reset_url = request.build_absolute_uri(reverse('userauths:password_reset_confirm', kwargs={'uidb64': uid, 'token': token}))
                    send_mail(
                        "Password Reset Request",
                        f"Please use the following link to reset your password: {reset_url}",
                        settings.DEFAULT_FROM_EMAIL,
                        [user.email]
                    )
                messages.success(request, "A password reset link has been sent to your email address.")
                return redirect('userauths:password_reset_done')
            else:
                messages.warning(request, "Email address not associated with any user.")
    else:
        form = PasswordResetForm()
    return render(request, 'userauths/password_reset.html', {'form': form})




def password_reset_done_view(request):
    return render(request, 'userauths/password_reset_done.html')






def password_reset_confirm_view(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode('utf-8')
        user = User.objects.get(pk=uid)
        if default_token_generator.check_token(user, token):
            if request.method == "POST":
                form = SetPasswordForm(user, request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Your password has been reset successfully.")
                    return redirect('userauths:sign-in')
            else:
                form = SetPasswordForm(user)
            return render(request, 'userauths/password_reset_confirm.html', {'form': form})
        else:
            messages.warning(request, "The password reset link is invalid or has expired.")
            return redirect('userauths:password_reset')
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.warning(request, "The password reset link is invalid or has expired.")
        return redirect('userauths:password_reset')




# def password_reset_complete_view(request):
#     messages.success(request, "Your password has been reset successfully. Please sign in.")
#     return render(request, 'userauths/password_reset_complete.html')
