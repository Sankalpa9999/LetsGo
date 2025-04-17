from django.urls import path
from userauths import views
app_name = 'userauths'

app_name = 'user'

urlpatterns = [
    path('sign-up/',views.register_view,name='sign-up'),
    path('sign-in/',views.login_view,name='sign-in'),
    path('sign-out/',views.logout_view,name='sign-out'),
    
    
    # path('profile/', views.user_profile, name='profile'),
    # path('edit-profile/', views.edit_profile, name='edit_profile'),
    
    path('profile/', views.user_profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
]