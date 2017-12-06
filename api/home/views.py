from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from .models import users
from django.contrib.auth.models import User

# Create your views here.

def index(request):
    return render(request, 'home/index.html',{'page':"Home"})

def loginpage(request):
    return render(request, 'home/login.html',{'page':"Login"})

def signuppage(request):
    return render(request, 'home/signup.html',{'page':"Sign-up"})

def logout(request):
    auth_logout(request)
    return render(request, 'home/signup.html', {'page': "Sign-up"})

def profile(request):
    #if request.user.is_authenticated == True:
    user=users.objects.get(user=request.user)
    return render(request, 'home/profile.html',{'page':request.user.username,'user':user})
    #return render(request, 'home/login.html',{'page':"Login"})

def login(request):
    username=request.POST['username']
    password=request.POST['password']

    user = authenticate(username=username, password=password)
    if user is not None:
        #print("shit")
        if user.is_active:
            auth_login(request, user)
            return redirect('/profile')
    return render(request, 'home/login.html',{'page':"Login"})


def UserFormView(request):
    template_name='home/signup.html'


    # process form data
    if request.method == 'POST':


        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        user=User(username=username,email=email)
        user.set_password(password)
        temp = authenticate(email=email)
        if temp is not None:
            return render(request, template_name, {'page':"Sign-up"})
        user.save()

        #print('pass')
        # returns User objects if credentials are correct
        user = authenticate(username=username,password=password)
        if user is not None:
            if user.is_active:
                auth_login(request.user)
                t = User.objects.get(username=username)
                new_entry=users(user=t,first_name=first_name,last_name=last_name)
                new_entry.save()
                return redirect('/profile')


        return render(request, template_name, {'page':"Sign-up"})