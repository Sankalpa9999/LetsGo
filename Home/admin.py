from django.contrib import admin
from Home.models import Product, Category, Department, Vendor, RentOrder, RentOrderItems, ProductImages, ProductReview, Wishlist, Address, DocumentImage, TermsAndConditions

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
    
class wishlistAdmin(admin.ModelAdmin):
    list_display = ['user','product','date']
    
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user','address','status']
    
    
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(RentOrder, RentOrderAdmin)
admin.site.register(RentOrderItems, RentOrderItemsAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Wishlist, wishlistAdmin)
admin.site.register(Address, AddressAdmin)
# admin.site.register(ProductDocuments)