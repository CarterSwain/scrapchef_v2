"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.shortcuts import render
from allauth.account.views import LogoutView
from accounts.views import logout_view, profile_view
from django.conf import settings
from django.conf.urls.static import static

# Simple home view
def home_view(request):
    return render(request, "home.html")

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home_view, name='home'),
    
    # Your custom accounts URLs
    path("accounts/", include("accounts.urls")),

    # Django Allauth for authentication
    path('accounts/', include('allauth.urls')),   # Django Allauth authentication URLs

    # Custom Logout view (No need to redefine logout_view)
    path("accounts/logout/", LogoutView.as_view(template_name="account/logout.html"), name="account_logout"),

    # Custom Profile view (No need to redefine profile_view)
    path("profile/", profile_view, name="profile"),
    
    # Recipes app
    path("recipes/", include("recipes.urls")),
    
    # Profiles app
    path('profiles/', include('profiles.urls', namespace='profiles')),
    
    # Explore app
    path("explore/", include("explore.urls")),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)