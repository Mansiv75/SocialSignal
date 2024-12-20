"""
URL configuration for SocialSignal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core.views import *
from allauth.socialaccount.providers.google.views import oauth2_login
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('', home_page, name="home"),
    path('admin/', admin.site.urls),
    path('login/', login_page, name="login"),
    path('register/', register_page, name="register"),
    path('logout/', logout_page, name="logout"),
    path('accounts/', include('allauth.urls')),
    path('github-login/', github_login, name="github"),
    path('twitter-data/', fetch_twitterdata, name="twitter"),
    path('google-login/', custom_google_login, name='google-login'),
    path('login/twitter/', lambda request: redirect('/accounts/twitter/login/')),
    path('auth/', include('social_django.urls')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
