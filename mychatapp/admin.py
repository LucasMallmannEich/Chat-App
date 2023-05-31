from django.contrib import admin
from mychatapp.models import Profile, Friend, ChatMessage

admin.site.register([Profile, Friend, ChatMessage])
