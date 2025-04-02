from Home.models import Product, Category, Department, Vendor, CartOrder, CartOrderItems, ProductImages, ProductReview, wishlist, Address

def default(request):
    categories = Category.objects.all()
    departments = Department.objects.all()
    vendors = Vendor.objects.all()
    Products = Product.objects.all()
    
    
    user_address = None
    if request.user.is_authenticated:  # Check if user is logged in
        user_address = Address.objects.filter(user=request.user, status=True).first()
    
    return {
        'categories':categories,
        'departments':departments,
        'vendors':vendors,
        'user_address': user_address,  # Pass as user_address
        'Products':Products,
        }