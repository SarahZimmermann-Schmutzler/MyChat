from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render
from .models import Message
from .models import Chat
from django.contrib.auth.decorators import login_required
from django.core import serializers

# Create your views here.


@login_required(login_url='/login/')
def index(request):
    """
    this is a view to render the chat html
    """
    if request.method == 'POST':
        print("Received Data " + request.POST['textmessage'])
        testChat = Chat.objects.get(id=1)
        # testChat ist jetzt immer Chat mit id=1 (manuell angelegt) --> später dynamisieren
        new_message = Message.objects.create(text=request.POST['textmessage'], chat=testChat, author=request.user, receiver=request.user)
        # Input von Chat-Seite wird in Datenbank als neues Objekt gespeichert
        serialized_obj = serializers.serialize('json', [new_message])
        # wandeln erstelltes Objekt in JSON um
        return JsonResponse(serialized_obj[1:-1], safe=False)
        # response ist String in Array --> nehmen dessen Substring, den wir umwandeln
    chatMessages = Message.objects.filter(chat__id=1)
    return render(request, 'chat/index.html', {'messages': chatMessages})
    # der Pfad reicht aus, da immer automatisch im Templat Ordner nachgesehen wird
    # können der Funktion ein JSON-Objekt mitgeben --> Variable hardcode oder dynamisch, z.B. die Messages aus Chat 1