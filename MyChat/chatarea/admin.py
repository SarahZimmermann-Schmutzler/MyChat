from django.contrib import admin
from .models import Message, Chat

# Antatt alle Felder anzeigen zu lassen, kann man auch Auswahl treffen
class MessageAdmin(admin.ModelAdmin):
    fields = ('chat','text','created_at', 'author', 'receiver')
    # sehe nur noch diese Infos im Interface
    list_display = ('created_at', 'author', 'text', 'receiver')
    # zeigt Infos schon in Vorauswahl
    search_fields = ('text',)
    #kann Nachrichten nach Text filtern

# Register your models here.
admin.site.register(Message, MessageAdmin)
admin.site.register(Chat)
