from django.urls import path
from . import views


app_name = 'message'


urlpatterns = [
    path('chat/', views.chat_list, name='chat_list'),
    path('chat/<int:user_id>/', views.chat_detail, name='chat_detail'),
    
    # Owner chat (add distinct path, e.g., "chat/owner/")
    path('chat/owner/', views.chat_list1, name='chat_list1'),
    path('chat/owner/<int:user_id>/', views.chat_detail1, name='chat_detail1'),
]
