from django.urls import path
from . import views


urlpatterns = [
    
    # index
    path('',views.index,name='index'),
    path('category/', views.category_list_view, name='category-list'),
    path('department/', views.department_list_view, name='department-list'),
    path('products/', views.product_list_view, name='product-list'),
    path('products/<pid>', views.product_detail_view, name='product-detail'),
    
    # list view
    path('category/<cid>/', views.category_product_list_view, name='category-product-list'),
    path('department/<did>/', views.department_category_list_view, name='department-category-list'),
    # path('about',views.about,name='about'),
    
    
    # vender view
    path('vendor/', views.vendor_list_view, name='vendor-list'),
    path('vendor/<vid>/', views.vendor_detail_view, name='vendor-detail'),
    
    path('contact/', views.contact, name='contact'),
    
    
    path('ajax-add-review/<str:pid>/', views.ajax_add_review, name='ajax-add-review'),
    
    
    path('search/', views.search_view, name='search'),
    
    path("add-to-cart/", views.add_to_cart, name="add-to-cart"),
    path('update-cart/', views.update_cart, name='update-cart'),
    
    path('rentlist/', views.cart_view, name='rentlist')
    # path('checkout/', views.checkout_view, name='checkout'),
    


]