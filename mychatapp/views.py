from django.shortcuts import render, redirect
from mychatapp.models import Profile, Friend, ChatMessage
from mychatapp.forms import ChatMessageForm
from django.http import JsonResponse
import json


def index(request):
    user = request.user.profile
    friends = user.friends.all()
    context = {'user': user, 'friends': friends}
    return render(request, 'mychatapp/index.html', context)


def details(request, pk):
    friend = Friend.objects.get(profile_id=pk)
    user = request.user.profile
    profile = Profile.objects.get(id=friend.profile.id)
    chats = ChatMessage.objects.all()
    recicle_chats = ChatMessage.objects.filter(msg_sender=profile, msg_receiver=user)  # i'm receiveing the msg
    recicle_chats.update(seen=True)
    form = ChatMessageForm()
    if request.method == 'POST':
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            chat_message = form.save(commit=False)
            chat_message.msg_sender = user
            chat_message.msg_receiver = profile
            chat_message.save()
            return redirect("rota_details", pk=friend.profile.id)
    context = {"friend": friend, "form": form, "user": user, "profile": profile, 'chats': chats,
               'num': recicle_chats.count()}
    return render(request, 'mychatapp/details.html', context)


def sentMessages(request, pk):
    user = request.user.profile
    friend = Friend.objects.get(profile_id=pk)
    profile = Profile.objects.get(id=friend.profile.id)
    data = json.loads(request.body)
    new_chat = data['msg']
    new_chat_message = ChatMessage.objects.create(body=new_chat, msg_sender=user, msg_receiver=profile, seen=False)
    print(new_chat)
    return JsonResponse(new_chat_message.body, safe=False)


def receivedMessages(request, pk):
    user = request.user.profile
    friend = Friend.objects.get(profile_id=pk)
    profile = Profile.objects.get(id=friend.profile.id)
    lista = []
    chats = ChatMessage.objects.filter(msg_sender=profile, msg_receiver=user)  # i'm receiveing the msg
    for chat in chats:
        lista.append(chat.body)  # getting the actual msg
    return JsonResponse(lista, safe=False)


def chatNotification(request):
    user = request.user.profile  # my profile
    friends = user.friends.all()  # my list of friends
    lista = []
    for friend in friends:  # for each friends in my friends list
        chats = ChatMessage.objects.filter(msg_sender__id=friend.profile.id, msg_receiver=user, seen=False)  # i'm receiveing the msg
        lista.append(chats.count())  # stores how many msgs we got from that one friend
    return JsonResponse(lista, safe=False)