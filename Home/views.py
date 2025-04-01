from math import prod
from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.db.models import Avg, Count
from stripe import Review
from Home.models import Product, Category, Department, Vendor, CartOrder, CartOrderItems, ProductImages, ProductReview, wishlist, Address
from django.contrib.auth.decorators import login_required

from Home.forms import ProductReviewForm
from django.template.loader import render_to_string


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



def product_detail_view(request, pid):
    product = Product.objects.get(pid = pid)
    product = get_object_or_404(Product, pid=pid)
    p_image = product.p_images.all()
    products = Product.objects.filter( product_status = "published", category = product.category).order_by('-id')
    
    review_form = ProductReviewForm()
    
    reviews = ProductReview.objects.filter(product=product).order_by('-date')
    average_rating = ProductReview.objects.filter(product=product).aggregate(rating = Avg('rating'))
    
    context = {
        'p':product,
        'products':products,
        'p_image':p_image,
        'reviews': reviews,
        'average_rating': average_rating,
        'review_form': review_form,
        }
    return render(request,'Land/product-detail.html', context)

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




