from django.shortcuts import redirect
from django.contrib import messages
from Home.models import Vendor
from functools import wraps
from django.urls import reverse

def vendor_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Please login first.")
            return redirect('userauths:sign-in')
            
        # Check if user is a vendor
        if not Vendor.objects.filter(user=request.user).exists():
            messages.error(request, "You need to be registered as a vendor to access this page.")
            return redirect('userauths:vendor_register')
            
        return function(request, *args, **kwargs)
    return wrap 