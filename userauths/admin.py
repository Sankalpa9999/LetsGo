from django.contrib import admin
from userauths.models import User, Profile, ContactUs
 
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('username','email','is_active','Bio')
    
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('image','full_name','phone')
    
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('name','subject')


admin.site.register(User, UserAdmin)
admin.site.register(Profile,ProfileAdmin)
admin.site.register(ContactUs, ContactUsAdmin)

