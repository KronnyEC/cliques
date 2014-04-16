from django.contrib import admin
from chat_server.models import ChatUser, ChatMessage
# Register your models here.


admin.site.register(ChatUser)
admin.site.register(ChatMessage)
