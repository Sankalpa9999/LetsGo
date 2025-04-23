from django.urls import path
from useradmin import views

app_name = 'useradmin'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    
    
    
    path('my-products/', views.vendor_product_list, name='vendor_product_list'),
    path('add-product/', views.add_product, name='add_product'),
    path('edit-product/<str:pid>/', views.edit_product, name='edit_product'),
    path('delete-product/<str:pid>/', views.delete_product, name='delete_product'),

    
    # Add other useradmin URLs here
]
