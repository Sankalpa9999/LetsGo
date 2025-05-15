from django.shortcuts import render, redirect, get_object_or_404
from Home.models import Product, Category, Department, Vendor, RentOrder, RentOrderItems, ProductImages, ProductReview, Wishlist, Address, RentOrderItems, RentalRequest
from userauths.models import User, Profile, ContactUs
from django.contrib import messages
from userauths.forms import UserRegisterForm,VendorRegistrationForm,UserUpdateForm



from django.contrib.auth.decorators import login_required
from useradmin.forms import ProductForm, ProductImageFormSet, DocumentImageFormSet, TermsAndConditionsFormSet,VendorForm



import datetime
# Create your views here.

def dashboard(request):
    return render(request, 'useradmin/dashboard.html')

@login_required
def vendor_product_list(request):
    vendors = Vendor.objects.filter(user=request.user)
    
    if not vendors.exists():
        messages.error(request, "No vendor accounts found.")
        return redirect('dashboard')

    # Optionally, pick the first one for now
    vendor = vendors.first()  # or prompt the user to select a vendor
    products = Product.objects.filter(vendor=vendor)
    return render(request, 'useradmin/vendor_product_list.html', {
        'products': products,
        'vendors': vendors,  # Send all if you want to let user choose
        'active_vendor': vendor,
    })



@login_required
def add_product(request):
    vendor = get_object_or_404(Vendor, user=request.user)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        image_formset = ProductImageFormSet(request.POST, request.FILES, prefix='images')
        doc_formset = DocumentImageFormSet(request.POST, request.FILES, prefix='docs')
        terms_formset = TermsAndConditionsFormSet(request.POST, request.FILES, prefix='terms')

        if form.is_valid() and image_formset.is_valid() and doc_formset.is_valid() and terms_formset.is_valid():
            product = form.save(commit=False)
            product.vendor = vendor
            product.user = request.user
            product.save()
            form.save_m2m()

            image_formset.instance = product
            image_formset.save()

            doc_formset.instance = product
            doc_formset.save()

            terms_formset.instance = product
            terms_formset.save()

            messages.success(request, "Product added successfully.")
            return redirect('/useradmin/my-products/')
    else:
        form = ProductForm()
        image_formset = ProductImageFormSet(prefix='images')
        doc_formset = DocumentImageFormSet(prefix='docs')
        terms_formset = TermsAndConditionsFormSet(prefix='terms')

    return render(request, 'useradmin/add_product.html', {
        'form': form,
        'image_formset': image_formset,
        'doc_formset': doc_formset,
        'terms_formset': terms_formset
    })


@login_required
def edit_product(request, pid):
    product = get_object_or_404(Product, pid=pid, vendor__user=request.user)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        image_formset = ProductImageFormSet(request.POST, request.FILES, instance=product, prefix='images')
        doc_formset = DocumentImageFormSet(request.POST, request.FILES, instance=product, prefix='docs')
        terms_formset = TermsAndConditionsFormSet(request.POST, request.FILES, instance=product, prefix='terms')

        if form.is_valid() and image_formset.is_valid() and doc_formset.is_valid() and terms_formset.is_valid():
            form.save()
            image_formset.save()
            doc_formset.save()
            terms_formset.save()
            messages.success(request, "Product updated successfully.")
            return redirect('/useradmin/my-products/')
    else:
        form = ProductForm(instance=product)
        image_formset = ProductImageFormSet(instance=product, prefix='images')
        doc_formset = DocumentImageFormSet(instance=product, prefix='docs')
        terms_formset = TermsAndConditionsFormSet(instance=product, prefix='terms')

    return render(request, 'useradmin/edit_product.html', {
        'form': form,
        'product': product,
        'image_formset': image_formset,
        'doc_formset': doc_formset,
        'terms_formset': terms_formset
    })
    
    
    
@login_required
def delete_product(request, pid):
    product = get_object_or_404(Product, pid=pid, vendor__user=request.user)
    product.delete()
    messages.success(request, "Product deleted successfully.")
    return redirect('/useradmin/my-products/')




@login_required
def vendor_rental_requests(request):
    vendor = get_object_or_404(Vendor, user=request.user)
    rental_requests = RentalRequest.objects.filter(product__vendor=vendor).order_by('-created_at')
    
    request.session['rental_request_data_count'] = rental_requests.count()
    
    return render(request, 'useradmin/vendor_rental_requests.html', {'rental_requests': rental_requests})

@login_required
def update_rental_status(request, request_id, action):
    vendor = get_object_or_404(Vendor, user=request.user)
    rental_request = get_object_or_404(RentalRequest, id=request_id, product__vendor=vendor)

    if action == 'accept':
        rental_request.status = 'Accepted'
        messages.success(request, "Request has been accepted successfully.")
    elif action == 'reject':
        rental_request.status = 'Rejected'
        messages.success(request, "Request has been rejected successfully.")
    
    rental_request.save()
    return redirect('/useradmin/requests/')



@login_required
def delete_rental_request(request, request_id):
    vendor = get_object_or_404(Vendor, user=request.user)
    rental_request = get_object_or_404(RentalRequest, id=request_id, product__vendor=vendor)

    if rental_request.status != 'Rejected':
        messages.warning(request, "You can only delete rejected requests.")
    else:
        rental_request.delete()
        messages.success(request, "Request deleted successfully.")

    return redirect('/useradmin/requests/')




@login_required
def requested_user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile, created = Profile.objects.get_or_create(user=user)

    return render(request, 'useradmin/requested_user_profile.html', {
        'profile': profile,
        'license_image': user.license_image,
        'citizenship_image': user.citizenship_image
    })
    

@login_required
def owner_profile(request):
    vendor = get_object_or_404(Vendor, user=request.user)

    context = {
        'vendor': vendor
    }
    return render(request, 'useradmin/owner_profile.html', context)
    
 

@login_required
def edit_owner_profile(request):
    vendor = get_object_or_404(Vendor, user=request.user)

    if request.method == 'POST':
        form = VendorRegistrationForm(request.POST, request.FILES, instance=vendor)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('useradmin:owner-profile') 
    else:
        form = VendorRegistrationForm(instance=vendor)

    context = {
        'form': form
    }
    return render(request, 'useradmin/edit_owner_profile.html', context)








@login_required
def vendor_rent_list_view(request):
    vendor = Vendor.objects.get(user=request.user)  

    rent_items = RentOrderItems.objects.all()
    # rent_items = RentOrderItems.objects.filter(product__vendor=vendor)
    request.session['rent_items_data_count'] = rent_items.count()

    context = {
        'rent_items': rent_items
    }
    return render(request, 'useradmin/vendor_rent_list.html', context)


from datetime import date

@login_required
def vendor_rent_history_view(request):
    vendor = get_object_or_404(Vendor, user=request.user)

    completed_items = RentOrderItems.objects.filter(
        product__vendor=vendor,
        Product_status='Completed'
    ).order_by('-return_date')

    request.session['completed_items_data_count'] = completed_items.count()
    
    context = {
        'history_items': completed_items
    }
    return render(request, 'useradmin/vendor_rent_history.html', context)

