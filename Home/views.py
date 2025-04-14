from math import prod
from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.db.models import Avg, Count
from stripe import Review
from Home.models import Product, Category, Department, Vendor, RentOrder, RentOrderItems, ProductImages, ProductReview, wishlist, Address, RentOrderItems
from django.contrib.auth.decorators import login_required

from Home.forms import ProductReviewForm
from django.contrib import messages
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from userauths import views



def index(request):
    # products = Product.objects.all().order_by('-id')
    products = Product.objects.filter(featured = True).order_by('-id')
    context = {
        'products':products
        }
    

    
    return render(request,'Land/index.html', context)  


def product_list_view(request):
    products = Product.objects.all().order_by('-id')
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
#     product = Product.objects.get(pid = pid)
#     product = get_object_or_404(Product, pid=pid)
#     p_image = product.p_images.all()
#     products = Product.objects.filter( product_status = "published", category = product.category).order_by('-id')
    
#     review_form = ProductReviewForm()
    
#     reviews = ProductReview.objects.filter(product=product).order_by('-date')
#     average_rating = ProductReview.objects.filter(product=product).aggregate(rating = Avg('rating'))
    
#     context = {
#         'p':product,
#         'products':products,
#         'p_image':p_image,
#         'reviews': reviews,
#         'average_rating': average_rating,
#         'review_form': review_form,
#         }
#     return render(request,'Land/product-detail.html', context)



def product_detail_view(request, pid):
    product = get_object_or_404(Product, pid=pid)  # This handles the 404 error automatically
    
    p_image = product.p_images.all()
    products = Product.objects.filter(product_status="published", category=product.category).order_by('-id')

    review_form = ProductReviewForm()
    reviews = ProductReview.objects.filter(product=product).order_by('-date')
    average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))

    context = {
        'p': product,
        'products': products,
        'p_image': p_image,
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
    
def contact(request):
    return render(request,'Land/contact.html')


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



    
    
    



# def add_to_cart(request):
#     if request.method == "POST":
#         product_id = str(request.POST.get('id'))
#         product_title = request.POST.get('title')
#         product_price = request.POST.get('price')
#         product_image = request.POST.get('image')  # Ensure image is captured
#         pid = request.POST.get('pid')

#         if not product_id or not product_title or not product_price:
#             return JsonResponse({'error': 'Invalid data'}, status=400)

#         cart_product = {
#             product_id: {
#                 'title': product_title,
#                 'price': product_price,
#                 'image': product_image  # Store image in session
#             }
#         }

#         if 'cart_data_obj' in request.session:
#             cart_data = request.session['cart_data_obj']
#             cart_data.update(cart_product)  # Update existing cart
#             request.session['cart_data_obj'] = cart_data
#         else:
#             request.session['cart_data_obj'] = cart_product  # Create new cart

#         return JsonResponse({
#             'data': request.session['cart_data_obj'],
#             'totalcartitems': len(request.session['cart_data_obj'])
#         })

#     return JsonResponse({'error': 'Invalid request'}, status=400)


# @require_POST
# def update_cart(request):
#     if request.method == "POST":
#         product_id = str(request.POST.get('product_id'))
#         action = request.POST.get('action')
        
#         if 'cart_data_obj' not in request.session:
#             return JsonResponse({'error': 'Cart not found'}, status=400)
            
#         cart_data = request.session['cart_data_obj']
        
#         if product_id not in cart_data:
#             return JsonResponse({'error': 'Product not in cart'}, status=400)
#         cart_data = request.session.get('cart_data_obj', {})
        
#         if action == 'remove':
#             if product_id in cart_data:
#                 del cart_data[product_id]
#                 request.session['cart_data_obj'] = cart_data
#                 request.session.modified = True
                
#                 # Calculate updated totals
#                 selected_items = {k: v for k, v in cart_data.items() if v.get('selected', True)}
#                 subtotal = sum(float(item['price']) for item in selected_items.values())
#                 service_fee = 5.00
#                 total = subtotal + service_fee
                
#                 return JsonResponse({
#                     'success': True,
#                     'subtotal': f"{subtotal:.2f}",
#                     'total': f"{total:.2f}",
#                     'selected_count': len(selected_items),
#                     'has_selected_items': len(selected_items) > 0,
#                     'totalcartitems': len(cart_data)
#                 })
#             return JsonResponse({'success': False, 'error': 'Product not in cart'})


#         elif action == 'toggle_select':
#             # Initialize selected if not exists
#             if 'selected' not in cart_data[product_id]:
#                 cart_data[product_id]['selected'] = True
#             # Toggle selection
#             cart_data[product_id]['selected'] = not cart_data[product_id]['selected']
        
#         request.session.modified = True
        
#         # Calculate updated totals
#         selected_items = {k: v for k, v in cart_data.items() if v.get('selected', True)}
#         subtotal = sum(float(item['price']) for item in selected_items.values())
#         service_fee = 5.00
#         total = subtotal + service_fee
        
#         return JsonResponse({
#             'success': True,
#             'subtotal': f"{subtotal:.2f}",
#             'total': f"{total:.2f}",
#             'selected_count': len(selected_items),
#             'has_selected_items': len(selected_items) > 0
#         })

#     return JsonResponse({'error': 'Invalid request'}, status=400)



# def cart_view(request):
#     cart_data = request.session.get('cart_data_obj', {})
    
#     # Ensure all items have a 'selected' key
#     for item in cart_data.values():
#         if 'selected' not in item:
#             item['selected'] = True
    
#     # Calculate totals
#     selected_items = {k: v for k, v in cart_data.items() if v.get('selected', True)}
#     subtotal = sum(float(item['price']) for item in selected_items.values())
#     service_fee = 100
#     total = subtotal + service_fee
    
#     context = {
#         'cart_data_obj': cart_data,
#         'selected_count': len(selected_items),
#         'subtotal': f"{subtotal:.2f}",
#         'service_fee': f"{service_fee:.2f}",
#         'total': f"{total:.2f}",
#         'has_selected_items': len(selected_items) > 0
#     }
#     return render(request, 'Land/rentlist.html', context)



def add_to_rentlist(request, pid):
    if request.method == 'POST':
        product = get_object_or_404(Product, pid=pid)
        rent_order, created = RentOrder.objects.get_or_create(
            user=request.user,
            paid_status=False,
            defaults={'price': product.price}
        )
        
        RentOrderItems.objects.create(
            order=rent_order,
            item=product.title,
            Product_status='Processing',
            image=product.image,
            qty=1,
            price=product.price,
            total=product.price,
            invoice_no=f"INV-{rent_order.id}-{RentOrderItems.objects.count() + 1}"
        )
        
        return redirect('rentlist')
    return redirect('product-detail', pid=pid)
def rentlist_view(request):
    if request.user.is_authenticated:
        rent_order = RentOrder.objects.filter(
            user=request.user, 
            paid_status=False
        ).prefetch_related(
            'rentorderitems_set'
        ).first()
        
        rent_items = []
        if rent_order:
            rent_items = RentOrderItems.objects.filter(
                order=rent_order
            ).select_related('order')
            
            # Add product to each rent item if available
            for item in rent_items:
                try:
                    item.product = Product.objects.get(title=item.item)
                except Product.DoesNotExist:
                    item.product = None
        
        context = {
            'rent_order': rent_order,
            'rent_items': rent_items,
        }
        return render(request, 'Land/rentlist.html', context)
    return redirect('login')