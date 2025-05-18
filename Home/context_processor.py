from Home.models import Product, Category, Department, Vendor, RentOrder, RentOrderItems, ProductImages, ProductReview, Wishlist, Address

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
    
    
# def rent_data_count(request):
#     rent_data_obj = request.session.get('rent_data_obj', [])
    
#     return {'rent_data_count': len(rent_data_obj)}

# def rent_list_count(request):
#     rent_count = 0
#     if request.user.is_authenticated:
#         try:
#             rent_order = RentOrder.objects.get(user=request.user, paid_status=False)
#             rent_count = RentOrderItems.objects.filter(order=rent_order).count()
#         except RentOrder.DoesNotExist:
#             pass
#     return {'rent_data_count': rent_count}



def base_template_context(request):
    if request.user.is_authenticated:
        # Check if user is a vendor
        is_vendor = Vendor.objects.filter(user=request.user).exists()
        
        # Check if the current URL is in the vendor registration process
        is_vendor_registration = request.path == '/user/register-vendor/'
        
        # Use adminbase.html only for vendors and not during registration
        if is_vendor and not is_vendor_registration:
            return {'base_template': 'partial/adminbase.html'}
    
    # Default to base.html for non-vendors and non-authenticated users
    return {'base_template': 'partial/base.html'}