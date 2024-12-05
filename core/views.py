from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from .social_media_service import *
# Create your views here.
def login_page(request):
    if request.method == 'POST':

        username=request.POST.get('username')
        password=request.POST.get('password')

        

        if not User.objects.filter(username=username).exists():
            messages.info(request, "Invalid Username")
            return redirect('/login/')
        
        user=authenticate(username=username, password=password)
        if user is None:
            messages.info(request, "Invalid Password")
            return redirect('/login/')
        
        else:
            login(request, user)
            messages.info(request, "Logged in successfully.")
            return redirect('/')


    return render(request, 'login.html')
def logout_page(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect('/login/')
def register_page(request):
    if request.method == 'POST':
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=User.objects.filter(username=username)

        if user.exists():
            messages.info(request, "Username already taken.")
            return redirect('/register/')

        user=User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username
            
        )
        user.set_password(password)
        user.save()
        messages.info(request, "Profile details updated.")
        return redirect('/register/')
    return render(request, 'register.html')


def fetch_githubdata(request):
    user=request.user
    github_service=GithubService(user)
    data=github_service.get_user_data
    return JsonResponse(data)

def fetch_twitterdata(request):
    user=request.user
    twitter_service=TwitterService(user)
    data=twitter_service.get_user_profile
    return JsonResponse(data)

def fetch_googledata(request):
    user=request.user
    google_service=GoogleService(user)
    data=google_service.get_user_profile
    return JsonResponse(data)