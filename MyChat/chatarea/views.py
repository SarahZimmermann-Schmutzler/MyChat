from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Message
from .models import Chat
from django.contrib.auth.decorators import login_required
from django.core import serializers

# Create your views here.


@login_required(login_url='/login/')
# ist User nicht eingeloggt, Weiterleitung zum Login
def index(request):
    """
    this is a view to create the data objects and render the chat html
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
        # response ist String in Array --> nehmen dessen Substring mit [1:-1] und wandeln ihn in der JS Funktion mit parse um
    chatMessages = Message.objects.filter(chat__id=1)
    return render(request, 'chat/index.html', {'messages': chatMessages})
    # der Pfad reicht aus, da immer automatisch im Templat Ordner nachgesehen wird
    # können der Funktion ein JSON-Objekt mitgeben --> Variable hardcode oder dynamisch, z.B. die Messages aus Chat 1


def render_login(request):
    """ 
    this is a view to render the login html and redirect logged users to the chat
    """
    redirect = request.GET.get('next')
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        # setzen in Authentifizierungsfunktion den username und password aus Frontend
        # binden es an Variable
        if user:
            login(request, user)
            # Login-Funktion
            return HttpResponseRedirect(request.POST.get('redirect', '/'))
            # existiert user, wird er eingeloggt und auf chat-seite weitergeleitet
        else:
            return render(request, 'auth/login.html', {'wrongPassword': True, 'redirect': request.POST.get('redirect', '/')})
            # existiert er nicht, gehts zurück auf login-seite
    return render(request, 'auth/login.html', {'redirect': redirect})
    # rendert die Seite login.html
    # übergeben die Variable redirect ins Frontend, um dort damit arbeiten zu können


def logout_user(request):
    """ 
    this is a view to render the logout html
    """
    if request.method == 'POST':
        logout(request)
    return render(request, 'auth/logout.html')


def render_register(request):
    """ 
    this is a view to render the register html and register new users
    """
    if request.method == 'POST':
        user = User.objects.create_user(username=request.POST.get('username'),
                                 email=request.POST.get('email'),
                                 password=request.POST.get('password'))
        if user:
            # return render(request, 'auth/login.html')
            return redirect('/')
        else:
            return render(request, 'auth/register.html')
    return render(request, 'auth/register.html')