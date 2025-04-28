

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







# def chat_detail(request, user_id):
#     other_user = get_object_or_404(User, id=user_id)

#     if request.method == 'POST':
#         message_text = request.POST.get('message')
#         if message_text:
#             Message.objects.create(sender=request.user, receiver=other_user, message=message_text)
#             messages.success(request, 'Message successfully sent!')
#             return redirect('message:chat_detail', user_id=other_user.id)

#     # Rename this to chat_messages instead of messages_qs
#     chat_messages = Message.objects.filter(
#         Q(sender=request.user, receiver=other_user) |
#         Q(sender=other_user, receiver=request.user)
#     ).order_by('timestamp')

#     base_template = 'partial/adminbase.html' if Vendor.objects.filter(user=request.user).exists() else 'partial/base.html'

#     return render(request, 'chat/chat_detail.html', {
#         'user': other_user,
#         'chat_messages': chat_messages,  # Changed variable name
#         'base_template': base_template,
#     })


def chat_detail(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        message_text = request.POST.get('message')
        uploaded_file = request.FILES.get('file')

        if message_text or uploaded_file:
            message_type = 'text'
            if uploaded_file:
                content_type = uploaded_file.content_type
                if content_type.startswith('image'):
                    message_type = 'image'
                elif content_type.startswith('video'):
                    message_type = 'video'
                else:
                    message_type = 'file'

            Message.objects.create(
                sender=request.user,
                receiver=other_user,
                message=message_text if message_type == 'text' else '',
                file=uploaded_file if uploaded_file else None,
                message_type=message_type,
            )
            messages.success(request, 'Message successfully sent!')
            return redirect('message:chat_detail', user_id=other_user.id)

    chat_messages = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    ).order_by('timestamp')

    base_template = 'partial/adminbase.html' if Vendor.objects.filter(user=request.user).exists() else 'partial/base.html'

    return render(request, 'chat/chat_detail.html', {
        'user': other_user,
        'chat_messages': chat_messages,
        'base_template': base_template,
    })