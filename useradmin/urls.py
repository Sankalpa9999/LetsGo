from django.urls import path
from useradmin import views


app_name = 'useradmin'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    
    
    
    path('my-products/', views.vendor_product_list, name='vendor_product_list'),
    path('add-product/', views.add_product, name='add_product'),
    path('edit-product/<str:pid>/', views.edit_product, name='edit_product'),
    path('delete-product/<str:pid>/', views.delete_product, name='delete_product'),
    
    
    
    
    path('requests/', views.vendor_rental_requests, name='vendor_rental_requests'),
    path('requests/<int:request_id>/<str:action>/', views.update_rental_status, name='update_rental_status'),
    path('requests/delete/<int:request_id>/', views.delete_rental_request, name='delete_rental_request'),
    
    
    path('requested-user-profile/<int:user_id>/', views.requested_user_profile, name='requested_user_profile'),
    
    
    path('owner/profile/', views.owner_profile, name='owner-profile'),
    path('owner/profile/edit/', views.edit_owner_profile, name='edit-owner-profile'),
    
    
    
    path('vendor/rent-list/', views.vendor_rent_list_view, name='vendor_rent_list'),
    path('vendor/rent-history/', views.vendor_rent_history_view, name='vendor_rent_history'),
    
]





    


