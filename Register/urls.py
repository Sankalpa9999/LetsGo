from django.urls import path
from . import views


urlpatterns = [
   path('joinpage/',views.joinpage, name= 'joinpage'), 

]
