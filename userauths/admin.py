from django.contrib import admin
from userauths.models import User, Profile, ContactUs
 

from django.utils.html import format_html



class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'Bio', 'profile_image', 'license_image', 'citizenship_image')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Profile Images', {'fields': ('profile_image', 'license_image', 'citizenship_image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'phone', 'verified')





    
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('name','subject')


admin.site.register(User, UserAdmin)
admin.site.register(Profile,ProfileAdmin)
admin.site.register(ContactUs, ContactUsAdmin)

