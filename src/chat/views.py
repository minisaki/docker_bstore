from django.shortcuts import render
from django.contrib.auth.models import User
# Create your views here.


def chat_view(request, user_id):
    user = User.objects.get(id=user_id)
    return render(request, 'chat/chat.html', {'user': user})