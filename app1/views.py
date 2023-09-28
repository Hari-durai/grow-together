from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import room,topic,Message
from .forms import RoomForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Q #filter table to get values using and,or keys
# Create your views here.
# value=[
#     {'id':1,'name':'Hari1'},
#     {'id':2,'name':'Hari2'},
#     {'id':3,'name':'Hari3'}
# ]
def loginpage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
        usernames=request.POST.get('username')
        password=request.POST.get('password')
        try:
            user=User.objects.get(username=usernames)
        except:
            messages.error(request,'Username or password not exsit')
        user=authenticate(request,username=usernames,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Username or password not exsit')
    content={"log":page}
    return render(request,'app1/login.html',content)
def register(request):
    page='register'
    use=UserCreationForm()
    if request.method=='POST':
        use=UserCreationForm(request.POST)
        if use.is_valid():
            user=use.save(commit=False) #commit so we can access internally (user)
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Invalid input')
    return render(request,'app1/login.html',{'log':page,'use':use})
def logoutpage(request):
    logout(request)
    return redirect('home')
def Home(request):
    q=request.GET.get('q') if request.GET.get('q') else ''
    val=room.objects.filter(Q(top__name__icontains=q) | Q(name__icontains=q) )#Q for & | keys parent (topic) class name noncase sense=i contain q value
    val1=topic.objects.all()
    coun=val.count()
    recent=Message.objects.filter(Q(room__top__name__icontains=q))
    value={'value':val,'val1':val1,'count':coun,'recent':recent}
    return render(request,'app1/home.html',value)


def root(request,ky):
    val=room.objects.get(id=ky)
    msg=val.message_set.all().order_by('-create')#take (Message) child of particular room (id) .(give small) M->message_set()
    value={'value':val,'msg':msg}
    if request.method=='POST':
        m=Message.objects.create(
            user=request.user,
            room=val,
            body=request.POST.get('body')
        )
        return redirect('root',ky=val.id)
    # val=None
    # for e in value:
    #     if e['id']==int(ky):
    #         val=e 
    
    return render(request,'app1/root.html',value)
@login_required(login_url='login')
def createroom(request):
    form=RoomForm() #empty form
    if request.method == 'POST':
        form=RoomForm(request.POST) #filled one in html
        if form.is_valid():            #     print(request.POST) # there is inbuild form validation
            rom=form.save(commit=False) #commit we use internally
            rom.host=request.user
            rom.save()
            return redirect('home')

    context={'form':form}
    return render(request,'app1/form.html',context)
@login_required(login_url='login')
def updateroom(request,pk):
    ro=room.objects.get(id=pk)
    form=RoomForm(instance=ro) #form pre filled
    if request.user!=ro.host:
        return HttpResponse('You are not allowed here')
    if request.method == 'POST':
        form=RoomForm(request.POST,instance=ro) #filled one in html
        if form.is_valid():            #     print(request.POST) # there is inbuild form validation
            form.save()
            return redirect('home')

    context={'form':form}
    return render(request,'app1/form.html',context)

def deleteform(request,ky):
    ro=room.objects.get(id=ky)
    if request.method=='POST':
        ro.delete()
        return redirect('home')
    return render(request,'app1/delete.html',{'obj':ro})

def deletecomment(request,ky):
    msg=Message.objects.get(id=ky)
    if request.user != msg.user:
        return HttpResponse("You are Not able to delete")
    if request.method=='POST': #it works only submit in form
        msg.delete()
        return redirect('home')
    return render(request,'app1/delete.html',{'obj':msg}) #this page return then go to post of msg delete

def userprofile(request,pk):
    host=User.objects.get(id=pk)
    val1=topic.objects.all()
    activity=host.message_set.all()
    ro=host.room_set.all()
    context={'host':host,'value':ro,'val1':val1,'recent':activity}
    return render(request,'app1/profile.html',context)
    

    