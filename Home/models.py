from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.safestring import mark_safe

from userauths.models import User

from taggit.managers import TaggableManager

from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

STATUS_CHOICE = (
    ('process', 'Processing'),
    ('shipped', 'Shipped'),
    ('delivered', 'Delivered'),
)
STATUS = (
    ('draft', 'Draft'),
    ('disabled', 'Disabled'),
    ('rejected', 'Rejected'),
    ('in_review', 'In Review'),
    ('published', 'Published'),
)
RATING = (
    (1, '★☆☆☆☆'),
    (2, '★★☆☆☆'),
    (3, '★★★☆☆'),
    (4, '★★★★☆'),
    (5, '★★★★★'),
)

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Department(models.Model):
    did = ShortUUIDField(unique=True, length=10, max_length=20, prefix='dat',alphabet='abcdefgh12345')
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='department', default='department.jpg')
    
    class Meta:
        verbose_name_plural = 'Departments'
        
    def department_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />'%(self.image.url))
    
    def __str__ (self):
        return self.title


class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=20, prefix='cat',alphabet='abcdefgh12345')
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category', default='category.jpg')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        
    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />'%(self.image.url))
    
    def __str__ (self):
        return self.title
        
class Tags(models.Model):
    pass

class Vendor(models.Model):
    vid = ShortUUIDField(unique=True, length=10, max_length=20, prefix='ven',alphabet='abcdefgh12345')
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to=user_directory_path, default='vendor.jpg')
    cover_image = models.ImageField(upload_to=user_directory_path, default='vendor.jpg')
    # user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    # description = models.TextField(null=True, blank=True)
    
    description = RichTextUploadingField(null=True, blank=True)
    
    
    address = models.CharField(max_length=100, null=True, blank=True, default='Pokhara')
    contact = models.CharField(max_length=100, null=True, blank=True, default='977-9000000')   
    chat_resp_time = models.CharField(max_length=100, null=True, blank=True, default='10:00 AM - 5:00 PM')
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    authentic_rating = models.CharField(max_length=100, null=True, blank=True, default='100')
    
    
    class Meta:
        verbose_name = 'Owner'
        verbose_name_plural = 'Owners'
     
    def vendor_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />'%(self.image.url))
    
    def __str__(self):
        return self.title 
    

class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=20,alphabet='abcdefgh12345')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True, related_name='vendor')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='department')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='category')
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to=user_directory_path, default='product.jpg')
    
    

    
    # description = models.TextField(null=True, blank=True)
    description = RichTextUploadingField(null=True, blank=True)
    
    price = models.DecimalField(max_digits=10, decimal_places=2)

    old_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # specifications = models.TextField(null=True, blank=True)
    specifications = RichTextUploadingField(null=True, blank=True)
    
    
    # Tags = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True)
    product_status = models.CharField(choices= STATUS, max_length=100, default='in_review')
    status = models.BooleanField(default=True)
    # in_stock = models.BooleanField(default=False)
    # digital = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    sku = ShortUUIDField(unique=True, length=10, max_length=20, prefix = "sku", alphabet='abcdefgh12345')
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True) 
    numberp = models.CharField(max_length=100, null=True, blank=True, default='ga 1 pa 1111')
    # stock_count = models.IntegerField(default=1)
    
    tags = TaggableManager(blank=True)
    
    
    class Meta:
        verbose_name_plural = 'Products'
        
    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />'%(self.image.url))
    


    
    
    def __str__ (self):
        return self.title
    
    def get_percentage(self):
        if self.old_price > self.price:  # Ensure old_price is greater to avoid negative or incorrect values
            discount_percentage = ((self.old_price - self.price) / self.old_price) * 100
            return round(discount_percentage, 2)  # Round to 2 decimal places
        return 0  # Return 0 if there's no discount

    
class ProductImages(models.Model):
    product = models.ForeignKey(Product, related_name='p_images', on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to="product-images", default='product.jpg', null = True,)
    date = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    
    class Meta:
        verbose_name_plural = 'Product Images'
        
class DocumentImage(models.Model):
    product = models.ForeignKey(Product, related_name='documents', on_delete=models.CASCADE, null=True)
    document = models.FileField(upload_to="product-images", null=True, blank=True)
    # doc_image = models.ImageField(upload_to="product-images", default='doc.jpg')
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Product Documents'

    def __str__(self):
        return f"Document for {self.product.title}"
    
class TermsAndConditions(models.Model):
    product = models.ForeignKey(Product, related_name='terms', on_delete=models.CASCADE)  # Add this line
    term_image = models.ImageField(upload_to="product-images", default='terms.jpg')
    description = RichTextUploadingField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Terms and Conditions'
        
    def __str__(self):
        return f"Terms for {self.product.title}"


   
class RentOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices= STATUS_CHOICE, max_length=100, default='Processing')
    
    class Meta:
        verbose_name_plural = 'Rent Order'
        
        
class RentOrderItems(models.Model):
    order = models.ForeignKey(RentOrder, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=200)
    Product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.ImageField(upload_to="Rent-order", default='product.jpg')
    qty = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2,default=100)
    
    
    class Meta:
        verbose_name_plural = 'Rent Order Items'
        
    def order_image(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />'%(self.image))
    
    
class ProductReview(models.Model): 
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name='reviews')
    
    rating = models.PositiveSmallIntegerField(choices=RATING, default=3)  # Use CharField instead of IntegerField
    
    review = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Product Reviews'
                
    def __str__(self):
        return str(self.rating)
    
    def get_rating(self):
        return self.rating



    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Wishlist'
         
    def __str__(self):
        return self.product.title if self.product else "No Product"
    
class Address(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=200 , null=True, blank=True)
    status = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = 'Address'
        
        
class RentalRequest(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rent_date = models.DateField()
    return_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.item} ({self.status})"
    
