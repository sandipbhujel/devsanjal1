from http.client import HTTPResponse
from multiprocessing import context
from pydoc import pager
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q
from .models import Room, Topic
from .forms import RoomForm
from django.contrib.auth import authenticate,login,logout
# Create your views here.

'''rooms = [
    {'id':1, 'name': 'Lets learn python'},
    {'id':2, 'name': 'Design with me'},
    {'id':3, 'name': 'Front end developer'},
]
'''

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request, 'User does not exist')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'username Or password doesnot exists')
    context = {'page':page}
    return render(request, 'base/login_register.html', context)

def logOutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    page = 'register'
    return render(request, 'base/login_register.html') 

def home(request):
    #rooms = Room.objects.all()
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    #rooms = Room.objects.filter(topic__name=q)
    #rooms = Room.objects.filter(topic__name__icontains=q)
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q)|
        Q(description__icontains=q)
    )
    room_count = rooms.count()
    topics = Topic.objects.all()
    context = {'rooms':rooms, 'topics':topics, 'room_count': room_count}
    return render(request, 'base/home.html', context)

def room(request,pk):
    '''room = None
    for i in rooms:
        if i['id'] == int(pk):
            room = i'''
    room = Room.objects.get(id=pk)
    context = {'room' : room}
    return render(request, 'base/room.html',context)

@login_required(login_url='login-page')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        #print(request.POST)
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request, 'base/form.html', context)

@login_required(login_url='login-page')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance = room)

    if request.user != room.host:
        return HttpResponse('You are not allowed')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/form.html',context)
    

@login_required(login_url='login-page')
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('You are not allowed')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render (request, 'base/delete.html',{'obj':room})
