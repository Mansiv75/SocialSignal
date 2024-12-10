from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from .social_media_service import *
from django.contrib.auth.decorators import login_required
from django.urls import reverse
# Create your views here.

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.shortcuts import redirect
from allauth.socialaccount.providers.google.views import oauth2_login

from social_django.utils import psa


def home_page(request):
    print("Home page view called!")
    return render(request, 'index.html')

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
#@psa('social:complete')
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
        return redirect('/')
    return render(request, 'register.html')

@login_required
def fetch_githubdata(request):
    user=request.user
    github_service=GithubService(user)
    data=github_service.get_user_data
    return JsonResponse(data)

@login_required
def fetch_twitterdata(request):
    user=request.user
    twitter_service=TwitterService(user)
    data=twitter_service.get_user_profile
    return JsonResponse(data)

@login_required
def fetch_googledata(request):
    
    user=request.user
    google_service=GoogleService(user)
    data=google_service.get_user_profile
    return JsonResponse(data)


def custom_google_login(request):
    print("Direct Google Login view is accessed!")
    return oauth2_login(request)

"""
class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    
    Override the DefaultSocialAccountAdapter from allauth in order to associate
    the social account with a matching User automatically, skipping the email
    confirm form and existing email error
    
    def pre_social_login(self, request, sociallogin):
        user = User.objects.filter(email=sociallogin.user.email).first()
        if user and not sociallogin.is_existing:
            sociallogin.connect(request, user)"""


GITHUB_CLIENT_ID = "Ov23lizS6UehomBziAjR"
GITHUB_REDIRECT_URI = "http://127.0.0.1:8000/accounts/github/login/callback/"  # Change to your app's callback URL

def github_login(request):
    return redirect(f"https://github.com/login/oauth/authorize?client_id={GITHUB_CLIENT_ID}&redirect_uri={GITHUB_REDIRECT_URI}")

