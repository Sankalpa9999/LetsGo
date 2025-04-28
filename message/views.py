

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from message.models import Message
from userauths.models import User
from Home.models import Vendor, Product
from django.db.models import Q
from django.template.loader import render_to_string
from django.http import JsonResponse
import json


@login_required
def chat_list(request):
    # Shows all users the logged-in user has chatted with
    users = User.objects.exclude(id=request.user.id)
    
    request.session['user_data_count'] = users.count()
    # Determine if the user is a Vendor
    base_template = 'partial/adminbase.html' if Vendor.objects.filter(user=request.user).exists() else 'partial/base.html'
    
    return render(request, 'chat/chat_list.html', {'users': users, 'base_template': base_template})





# @login_required
# def chat_detail(request, user_id):
#     user = User.objects.get(id=user_id)
#     messages = Message.objects.filter(
#         Q(sender=request.user, receiver=user) | Q(sender=user, receiver=request.user)
#     ).order_by('timestamp')

#     if request.method == 'POST':
#         new_message = request.POST.get('message')
#         if new_message:
#             Message.objects.create(sender=request.user, receiver=user, message=new_message)
#             return redirect('message:chat_detail', user_id=user.id)

#     return render(request, 'chat/chat_detail.html', {'user': user, 'messages': messages})



def chat_detail(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    # If form is submitted
    if request.method == 'POST':
        message_text = request.POST.get('message')
        if message_text:
            Message.objects.create(sender=request.user, receiver=other_user, message=message_text)
            messages.success(request, 'Message successfully sent!')
            return redirect('message:chat_detail', user_id=other_user.id)  # Corrected redirection

    messages_qs = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    ).order_by('timestamp')

    base_template = 'partial/adminbase.html' if Vendor.objects.filter(user=request.user).exists() else 'partial/base.html'

    return render(request, 'chat/chat_detail.html', {
        'user': other_user,
        'messages': messages_qs,
        'base_template': base_template,
    })