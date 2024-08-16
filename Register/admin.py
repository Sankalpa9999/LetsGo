from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name')
    search_fields = ('user__email', 'name')

# Alternatively, without the decorator
# admin.site.register(UserProfile, UserProfileAdmin)
