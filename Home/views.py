from math import prod
from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.db.models import Avg, Count
from stripe import Review
from Home.models import Product, Category, Department, Vendor, RentOrder, RentOrderItems, ProductImages, ProductReview, Wishlist, Address, RentOrderItems
from django.contrib.auth.decorators import login_required

from Home.forms import ProductReviewForm
from django.contrib import messages
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from userauths import views



def index(request):
    # products = Product.objects.all().order_by('-id')
    products = Product.objects.filter( product_status = "published").order_by('-id')
    # products = Product.objects.filter(featured = True, product_status = "Published").order_by('-id')
    context = {
        'products':products
        }
    

    
    return render(request,'Land/index.html', context)  


def product_list_view(request):
    products = Product.objects.filter( product_status = "published").order_by('-id')

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
    products = Product.objects.filter( product_status = "published", category = category).order_by('-id')
    context = {
        'category':category,
        'products':products,
        'department':department
        }
    
    return render(request,'Land/category-product-list.html', context)


def department_category_list_view(request, did):
    department = Department.objects.get(did = did)
    category = Category.objects.filter(department = department).order_by('-id')
    products = Product.objects.filter( product_status = "published", department = department).order_by('-id')

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
    products = Product.objects.filter( product_status = "published", vendor = vendor).order_by('-id')

    

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
            product_status="published",
            category__department=product.category.department
        ).exclude(id=product.id).order_by('-id')
    else:
        # If no category, fetch related products directly from the same department
        related_products = Product.objects.filter(
            product_status="published",
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
        products = Product.objects.filter(title__icontains=query).order_by('-date')
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



def remove_from_rent_list(request, item_id):
    if not request.user.is_authenticated:
        messages.warning(request, "You need to log in to perform this action.")
        return redirect('/user/sign-in/')

    item = get_object_or_404(RentOrderItems, id=item_id)

    if item.order.user == request.user:
        item.delete()
        # Remove item from session as well
        rent_data = request.session.get('rent_data_obj', [])
        rent_data = [entry for entry in rent_data if entry['title'] != item.item]
        request.session['rent_data_obj'] = rent_data  # Save updated session
        
        messages.success(request, "Item removed from your rent list.")
    else:
        messages.error(request, "Unauthorized action.")

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