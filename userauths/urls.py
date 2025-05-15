from django.urls import path,include
from userauths import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
app_name = 'userauths'






urlpatterns = [
    path('sign-up/',views.register_view,name='sign-up'),
    path('sign-in/',views.login_view,name='sign-in'),
    path('sign-out/',views.logout_view,name='sign-out'),
    
    
    # path('profile/', views.user_profile, name='profile'),
    # path('edit-profile/', views.edit_profile, name='edit_profile'),
    
    path('profile/', views.user_profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('change-password/', views.change_password, name='change_password'),
    
    
    path('register-vendor/', views.register_as_vendor, name='vendor_register'),

    
    
    
    path('contact/', views.contactUs, name='contact'),
    
    path('', include('django.contrib.auth.urls')),

    
    path('password-reset/', views.password_reset_view, name='password_reset'),
    path('password-reset/done/', views.password_reset_done_view, name='password_reset_done'),
    path(
    'user/reset/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(
        success_url=reverse_lazy('userauths:sign-in')
    ),
    name='password_reset_confirm'
),
    # path('reset-password/complete/', views.password_reset_complete_view, name='password_reset_complete'),

    # path('password-reset/done/', views.password_reset_complete_view, name='password_reset_complete'),


    
]
    
    
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)