from django.urls import path
from userauths import views
from django.conf import settings
from django.conf.urls.static import static


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
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)