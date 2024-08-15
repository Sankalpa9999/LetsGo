from django.urls import path
from . import views


urlpatterns = [
    path('sanjog/',views.sanjog, name= 'sanjog'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
 