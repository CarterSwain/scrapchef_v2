from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from allauth.account.forms import SignupForm
from django.contrib.auth.decorators import login_required
from allauth.socialaccount.models import SocialAccount

# Custom Register View (Using Django Allauth's SignupForm)
def register_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)  # Allauth signup form
        if form.is_valid():
            user = form.save(request)
            login(request, user)  # Log the user in
            return redirect("profile")  # Redirect to profile page after signup
    else:
        form = SignupForm()

    return render(request, "auth/register.html", {"form": form})

# Custom Login View (If not using Allauth's login)
def login_view(request):
    if request.user.is_authenticated:
        return redirect("profile")  # Redirect if already logged in

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("profile")
    else:
        form = AuthenticationForm()

    return render(request, "auth/login.html", {"form": form})

# Logout View (Now Handles Google Logout)
def logout_view(request):
    if request.user.is_authenticated:
        # Remove any linked social accounts (Fixes Google Logout Issues)
        SocialAccount.objects.filter(user=request.user).delete()
        
        # Log the user out
        logout(request)

        # Clear session data
        request.session.flush()

    return redirect("home")  # Redirect to home after logout

# Protected Profile Page
@login_required
def profile_view(request):
    return render(request, "account/profile.html", {"user": request.user})
