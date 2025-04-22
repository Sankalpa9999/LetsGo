from django.shortcuts import render, redirect, get_object_or_404
from Home.models import Product, Category, Department, Vendor, RentOrder, RentOrderItems, ProductImages, ProductReview, Wishlist, Address, RentOrderItems 
from django.db.models import Sum
from userauths.models import User, Profile
from django.contrib import messages


import datetime
# Create your views here.

def dashboard(request):
    return render(request, 'useradmin/dashboard.html')