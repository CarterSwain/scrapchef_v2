from django.urls import path
from .views import logout_view, profile_view

urlpatterns = [
    path("profile/", profile_view, name="profile"),
    path("logout/", logout_view, name="account_logout"),  
]


