from Home.models import Product, Category, Department, Vendor, CartOrder, CartOrderItems, ProductImages, ProductReview, wishlist, Address

def default(request):
    categories = Category.objects.all()
    departments = Department.objects.all()
    vendors = Vendor.objects.all()
    
    return {
        'categories':categories,
        'departments':departments,
        'vendors':vendors,
        }