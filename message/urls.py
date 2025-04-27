from django.urls import path
from . import views


app_name = 'message'


urlpatterns = [
    path('chat/', views.chat_list, name='chat_list'),
    path('chat/<int:user_id>/', views.chat_detail, name='chat_detail'),
]
