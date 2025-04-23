from django.contrib import admin
from Home.models import Product, Category, Department, Vendor, RentOrder, RentOrderItems, ProductImages, ProductReview, Wishlist, Address, DocumentImage, TermsAndConditions, RentalRequest

# Register your models here.

class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages
    
class DocumentImageAdmin(admin.TabularInline):
    model = DocumentImage
    extra = 1

class TermsAndConditionsAdmin(admin.TabularInline):
    model = TermsAndConditions
    extra = 1

    
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin, DocumentImageAdmin, TermsAndConditionsAdmin]
    
    list_display = ['pid','title', 'product_image', 'price','category','vendor', 'featured', 'product_status']
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title','category_image']
    
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['title','department_image']
    
class VendorAdmin(admin.ModelAdmin):
    list_display = ['title','vendor_image']
    
class RentOrderAdmin(admin.ModelAdmin):
    list_display = ['user','price','paid_status','order_date', 'product_status']
    
class RentOrderItemsAdmin(admin.ModelAdmin):
    list_display = ['order','invoice_no','item','image','qty','price','total']
    
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'review')
    
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'date']
    
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user','address','status']
    
    
    



class RentalRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rent_date', 'return_date', 'total_days', 'status', 'total_price')
    list_filter = ('status',)
    search_fields = ('user__username', 'product__title')

    def total_days(self, obj):
        """Calculate the total days of the rental."""
        return (obj.return_date - obj.rent_date).days
    total_days.short_description = 'Total Days'  # Set column name in the admin list view

    
    
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(RentOrder, RentOrderAdmin)
admin.site.register(RentOrderItems, RentOrderItemsAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(RentalRequest, RentalRequestAdmin)
# admin.site.register(ProductDocuments)