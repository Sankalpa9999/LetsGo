

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from message.models import Message
from userauths.models import User
from Home.models import Vendor, Product
from django.db.models import Q




@login_required
def chat_list(request):
    # Shows all users the logged-in user has chatted with
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'chat/chat_list.html', {'users': users})

@login_required
def chat_detail(request, user_id):
    user = User.objects.get(id=user_id)
    messages = Message.objects.filter(
        Q(sender=request.user, receiver=user) | Q(sender=user, receiver=request.user)
    ).order_by('timestamp')

    if request.method == 'POST':
        new_message = request.POST.get('message')
        if new_message:
            Message.objects.create(sender=request.user, receiver=user, message=new_message)
            return redirect('message:chat_detail', user_id=user.id)

    return render(request, 'chat/chat_detail.html', {'user': user, 'messages': messages})

