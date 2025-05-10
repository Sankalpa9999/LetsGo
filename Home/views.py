from math import prod

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from stripe import Review
from decimal import Decimal
import uuid
import base64
from decimal import Decimal
from django.conf import settings


from django.views.decorators.csrf import csrf_exempt

from Home.forms import ProductReviewForm, RentalRequestForm
from Home.models import (Address, Category, Department, Product, ProductImages,
                         ProductReview, RentOrder, RentOrderItems, Vendor,
                         Wishlist, RentalRequest)
from userauths import views
from datetime import timedelta


def index(request):
    # products = Product.objects.all().order_by('-id')
    products = Product.objects.filter( product_status = "published",featured = True).order_by('-id')
    # products = Product.objects.filter(featured = True, product_status = "Published").order_by('-id')
    context = {
        'products':products
        }
    

    
    return render(request,'Land/index.html', context)  


def product_list_view(request):
    products = Product.objects.filter( product_status = "published",featured = True).order_by('-id')

    # products = Product.objects.filter(product_status = "Published").order_by('-id')
    context = {
        'products':products
        }
    
    return render(request,'Land/product-list.html', context)  


def category_list_view(request):
    categories = Category.objects.all()

    context = {
        'categories':categories,


        }
    return render(request,'Land/category-list.html', context)


def department_list_view(request):
    departments = Department.objects.all()
    context = {
        'departments':departments
        }
    return render(request,'Land/department-list.html', context)


def category_product_list_view(request, cid):
    category = Category.objects.get(cid = cid)
    department = Department.objects.filter(category = category).order_by('-id')
    products = Product.objects.filter( product_status = "published",featured = True, category = category).order_by('-id')
    context = {
        'category':category,
        'products':products,
        'department':department
        }
    
    return render(request,'Land/category-product-list.html', context)


def department_category_list_view(request, did):
    department = Department.objects.get(did = did)
    category = Category.objects.filter(department = department).order_by('-id')
    products = Product.objects.filter( product_status = "published", featured = True, department = department).order_by('-id')

    context = {
        'category':category,
        'department':department,
        'products':products
        }
    
    return render(request,'Land/department-category-list.html', context)


def vendor_list_view(request):
    vendors = Vendor.objects.all()
    context = {
        'vendors':vendors
        }
    return render(request,'Land/vendor-list.html', context)


def vendor_detail_view(request, vid):
    vendor = Vendor.objects.get(vid = vid)
    products = Product.objects.filter( product_status = "published",featured = True, vendor = vendor).order_by('-id')

    

    context = {
        'vendor': vendor,
        'products': products,
        
    }

    return render(request,'Land/vendor-detail.html', context)





# def product_detail_view(request, pid):
#     product = get_object_or_404(Product, pid=pid)  # This handles the 404 error automatically
    
#     p_image = product.p_images.all()
#     products = Product.objects.filter(product_status="published", category=product.category).order_by('-id')

#     review_form = ProductReviewForm()
#     reviews = ProductReview.objects.filter(product=product).order_by('-date')
#     average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))

#     context = {
#         'p': product,
#         'products': products,
#         'p_image': p_image,
#         'reviews': reviews,
#         'average_rating': average_rating,
#         'review_form': review_form,
#     }
#     return render(request, 'Land/product-detail.html', context)



def product_detail_view(request, pid):
    product = get_object_or_404(Product, pid=pid)

    # Fetch related images, documents, and terms
    p_images = product.p_images.all()
    documents = product.documents.all()
    terms = product.terms.all()

    # Fetch related products from same 
    # related_products = Product.objects.filter(product_status="published",
    #     category=product.category
    # ).exclude(id=product.id).order_by('-id')
    
    # Fetch related products from the same department, even if the product doesn't have a category
    if product.category:
        related_products = Product.objects.filter(
            product_status="published",featured = True,
            category__department=product.category.department
        ).exclude(id=product.id).order_by('-id')
    else:
        # If no category, fetch related products directly from the same department
        related_products = Product.objects.filter(
            product_status="published",featured = True,
            department=product.department
        ).exclude(id=product.id).order_by('-id')


    # Review related data
    review_form = ProductReviewForm()
    reviews = ProductReview.objects.filter(product=product).order_by('-date')
    average_rating = reviews.aggregate(rating=Avg('rating'))

    context = {
        'p': product,
        'products': related_products,
        'p_images': p_images,
        'documents': documents,
        'terms': terms,
        'reviews': reviews,
        'average_rating': average_rating,
        'review_form': review_form,
    }
    return render(request, 'Land/product-detail.html', context)






def custom_404(request, exception):
    return render(request, 'Land/404.html', status=404)

@login_required
def ajax_add_review(request, pid):
    product = get_object_or_404(Product, pid=pid)
    user = request.user
    rating = int(request.POST['rating'])

    review = ProductReview.objects.create(
        product=product,
        user=user,
        review=request.POST['review'],
        rating=rating
    )

    average_reviews = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))

    # Generate star HTML for Ajax response
    star_html = ''.join(['&#9733;' if i < rating else '&#9734;' for i in range(5)])

    return JsonResponse({
        'bool': True,
        'user': user.username,
        'review': request.POST['review'],
        'rating': rating,
        'stars': star_html,
        'average_reviews': average_reviews,
        'user_has_reviewed': ProductReview.objects.filter(product=product, user=user).exists()
    })
    



def search_view(request):
    query = request.GET.get('q', '').strip()
    print(f"Search query: '{query}'")  # Debug print

    if query:
        products = Product.objects.filter(title__icontains=query, featured = True).order_by('-date')
        print(f"Found {products.count()} products")  # Debug print
    else:
        products = Product.objects.none()

    context = {
        'products': products,
        'query': query,
    }
    return render(request, 'Land/search.html', context)

    


# views.py

def add_to_rent(request, pid):
    if not request.user.is_authenticated:
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"message": "You need to login to rent a product.", "status": "error"})
        messages.warning(request, "You need to login to rent a product.")
        return redirect('/userauths/sign-in')

    product = get_object_or_404(Product, pid=pid)
    rent_order, created = RentOrder.objects.get_or_create(user=request.user, paid_status=False)

    existing_item = RentOrderItems.objects.filter(order=rent_order, item=product.title).first()
    if existing_item:
        return JsonResponse({"message": f"{product.title} is already in your rent list!", "status": "info"})

    RentOrderItems.objects.create(
        order=rent_order,
        invoice_no=f"INV{rent_order.id}{product.id}",
        Product_status=product.product_status,
        item=product.title,
        image=product.image,
        qty=1,
        price=product.price,
        total=product.price,
    )
    
    # Update session variable for rent data
    rent_data = request.session.get('rent_data_obj', [])
    rent_data.append({'title': product.title, 'pid': product.pid})
    request.session['rent_data_obj'] = rent_data  # Save updated session

    return JsonResponse({"message": f"{product.title} added to your rent list!", "status": "success"})



def rent_list_view(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Please log in to view your rent list.")
        return redirect('/user/sign-in/')

    try:
        rent_order = RentOrder.objects.get(user=request.user, paid_status=False)
        items = RentOrderItems.objects.filter(order=rent_order)

        # Map each item to the corresponding product pid
        item_list = []
        for item in items:
            product = Product.objects.filter(title=item.item).first()
            item_list.append({
                'item': item,
                'pid': product.pid if product else None,
                'vendor': product.vendor if product else None,
            })

    except RentOrder.DoesNotExist:
        rent_order = None
        item_list = []


    rent_data_obj = request.session.get('rent_data_obj', [])
    request.session['rent_data_count'] = len(rent_data_obj)  # Update session count
    

    
    context = {
        'rent_order': rent_order,
        'items': item_list,
        'rent_data_count': len(rent_data_obj),  # Pass the count of items in the rent list
    }
    return render(request, 'Land/rentlist.html', context)



# def remove_from_rent_list(request, item_id):
#     if not request.user.is_authenticated:
#         messages.warning(request, "You need to log in to perform this action.")
#         return redirect('/user/sign-in/')

#     item = get_object_or_404(RentOrderItems, id=item_id)

#     if item.order.user == request.user:
#         item.delete()
#         # Remove item from session as well
#         rent_data = request.session.get('rent_data_obj', [])
#         rent_data = [entry for entry in rent_data if entry['title'] != item.item]
#         request.session['rent_data_obj'] = rent_data  # Save updated session
        
#         messages.success(request, "Item removed from your rent list.")
#     else:
#         messages.error(request, "Unauthorized action.")

#     return redirect('rentlist')





def remove_from_rent_list(request, item_id):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        messages.warning(request, "You need to log in to perform this action.")
        return redirect('/user/sign-in/')
    
    # Get the RentOrderItem object based on item_id
    item = get_object_or_404(RentOrderItems, id=item_id)

    # Check if the item belongs to the logged-in user
    if item.order.user == request.user:
        # Remove the item from the database
        item.delete()

        # Remove the item from the session data
        rent_data = request.session.get('rent_data_obj', [])
        rent_data = [entry for entry in rent_data if entry['pid'] != item.id]  # Use the item ID here instead of title
        request.session['rent_data_obj'] = rent_data  # Save the updated session

        # Add a success message
        messages.success(request, "Item removed from your rent list.")
    else:
        # If the item does not belong to the user
        messages.error(request, "Unauthorized action.")

    # Redirect to the rent list page (ensure this URL name is correct)
    return redirect('rentlist')







    
    
    
@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    request.session['wishlist_data_count'] = wishlist_items.count() 

        
    context = {
        'w': wishlist_items,
     
    }
    return render(request, 'Land/wishlist.html', context)


@login_required
def add_to_wishlist(request):
    product_id = request.GET.get('id')
    product = get_object_or_404(Product, id=product_id)

    # Check if product is already in wishlist
    exists = Wishlist.objects.filter(product=product, user=request.user).exists()

    if exists:
        return JsonResponse({"bool": True, "message": "Already in wishlist"})
    else:
        Wishlist.objects.create(product=product, user=request.user)
        return JsonResponse({"bool": True, "message": "Added to wishlist"})

from django.views.decorators.csrf import csrf_exempt


@csrf_exempt  # Only for debugging, ideally use CSRF token properly
@require_POST
@login_required
def remove_from_wishlist(request, pid):
    if request.method == 'POST':
        product = get_object_or_404(Product, pid=pid)
        wishlist_item = Wishlist.objects.filter(user=request.user, product=product).first()
        if wishlist_item:
            wishlist_item.delete()
            messages.success(request, f"{product.title} removed from wishlist.")
        else:
            messages.error(request, "Item not found in wishlist.")
    return redirect('wishlist')




@login_required
def request_to_rent(request, pid):
    product = get_object_or_404(Product, pid=pid)

    # Check if user has already requested this product
    existing_rental = RentalRequest.objects.filter(user=request.user, product=product).first()
    if existing_rental:
        messages.warning(request, 'You have already requested this product.')
        return redirect('rent-request')
     
    
    if request.method == 'POST':
        form = RentalRequestForm(request.POST)
        if form.is_valid():
            rental = form.save(commit=False)
            rental.user = request.user
            rental.product = product

            rental.save()
            messages.success(request, 'Your rental request has been submitted!')
            return redirect('rent-request')
    else:
        form = RentalRequestForm()

    return render(request, 'land/request_form.html', {'form': form, 'product': product})



@login_required
def rentrequest_view(request):
    rental_requests = RentalRequest.objects.filter(user=request.user).order_by('-created_at')
    request.session['rental_request_data_count'] = rental_requests.count() 
    return render(request, 'land/rent-request.html', {'rental_requests': rental_requests})


@login_required
def edit_rent_request(request, id):
    rent_request = get_object_or_404(RentalRequest, id=id, user=request.user)

    if request.method == 'POST':
        form = RentalRequestForm(request.POST, instance=rent_request)
        if form.is_valid():
            form.save()
            messages.success(request, 'Rental request updated successfully.')
            return redirect('rent-request')
    else:
        form = RentalRequestForm(instance=rent_request)

    return render(request, 'land/request_form.html', {'form': form, 'product': rent_request.product, 'edit_mode': True})

@login_required
def delete_rent_request(request, id):
    rent_request = get_object_or_404(RentalRequest, id=id, user=request.user)

    # Delete directly (GET or POST — since no confirmation needed)
    rent_request.delete()
    messages.success(request, 'Rental request deleted.')
    return redirect('rent-request')



@login_required
def rental_checkout(request):
    if request.method == "POST":
        selected_ids = request.POST.getlist('selected_requests')
        rental_requests = RentalRequest.objects.filter(id__in=selected_ids)
        
        # Calculate the total amount as a Decimal
        total_amount = sum(Decimal(req.total_price) for req in rental_requests)
        
        # Use Decimal for 0.2 instead of float
        advance = total_amount * Decimal('0.2')

        # Convert the Decimal values to string or float for session storage
        request.session['rental_checkout'] = {
            'selected_ids': selected_ids,
            'total': str(total_amount),  # or float(total_amount)
            'advance': str(advance)  # or float(advance)
        }

        # Redirect to the payment page
        return redirect('rental_payment_page')
    
    return redirect('rent-request')




@login_required
def rental_payment_page(request):
    checkout_data = request.session.get('rental_checkout')
    if not checkout_data:
        messages.error(request, "No rental checkout data found.")
        return redirect('rent-request')

    # Unique order ID (e.g., for verification later)
    order_code = str(uuid.uuid4())[:8]  # You can store this in DB if needed

    amount = checkout_data.get('total')
    advance = checkout_data.get('advance')

    # Optionally save the order info in the database with status = pending

    # Build SkyPay checkout URL
    api_key = settings.SKYPAY_API_KEY  # Store securely in settings.py
    success_url = request.build_absolute_uri('/payment/success/')
    failure_url = request.build_absolute_uri('/payment/failure/')

    checkout_url = (
        f"https://checkout.skypay.dev?"
        f"api_key={api_key}&"
        f"amount={advance}&"
        f"code={order_code}&"
        f"success_url={success_url}&"
        f"failure_url={failure_url}"
    )

    return redirect(checkout_url)


import json
@login_required
@csrf_exempt
def payment_success(request):
    encoded_data = request.GET.get('data')
    if not encoded_data:
        messages.error(request, "No transaction data received.")
        return redirect('rent-request')

    # Decode base64 string to JSON
    try:
        decoded_bytes = base64.b64decode(encoded_data)
        decoded_data = json.loads(decoded_bytes)

        order_code = decoded_data.get('code')
        amount = Decimal(decoded_data.get('amount'))
        status = decoded_data.get('status')

        # TODO: verify order_code and mark rental as paid
        # Example: update database record with matching code
        if status == 'complete':
            messages.success(request, f"Payment successful! Order: {order_code}")
        else:
            messages.warning(request, f"Payment status: {status}")

    except Exception as e:
        messages.error(request, f"Error decoding payment: {e}")

    return redirect('rent-request')


@login_required
def payment_failure(request):
    message = request.GET.get('message', 'Payment failed.')
    messages.error(request, message)
    return redirect('rent-request')
