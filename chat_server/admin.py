from django.contrib import admin
from chat_server.models import ChatSession, ChatMessage


admin.site.register(ChatSession)
admin.site.register(ChatMessage)
